#!/usr/bin/env python3
# Copyright 2026 Zyvor AI Labs · https://zyvor.dev
# SPDX-License-Identifier: Apache-2.0
"""Ephemeral peer stubs that speak the real Yard connector contracts.

Runs in-process HTTP servers for Device Agent, Nodra, Fleet, and a Yard
ingest sink so suite_smoke.py can prove the cross-product paths without
building every binary on every PR.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable
from urllib.parse import urlparse


def _json(handler: BaseHTTPRequestHandler, code: int, body: Any) -> None:
    raw = json.dumps(body).encode()
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def _read_json(handler: BaseHTTPRequestHandler) -> Any:
    n = int(handler.headers.get("Content-Length") or "0")
    if n <= 0:
        return None
    return json.loads(handler.rfile.read(n))


def _auth_ok(handler: BaseHTTPRequestHandler, expected: str) -> bool:
    auth = handler.headers.get("Authorization", "")
    return auth == f"Bearer {expected}"


class PeerState:
    def __init__(self) -> None:
        self.yard_inventory: list[dict[str, Any]] = []
        self.yard_observations: list[Any] = []
        self.hits: list[str] = []


def make_handler(
    kind: str, token: str, state: PeerState
) -> Callable[[Any, Any, Any], BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt: str, *args: Any) -> None:  # quiet CI logs
            return

        def do_GET(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            state.hits.append(f"GET {kind}{path}")
            if kind == "device-agent":
                if path in ("/api/v1/health", "/healthz"):
                    return _json(
                        self,
                        200,
                        {
                            "status": "ok",
                            "serial": "ZY-SUITE-DA",
                            "version": "suite-stub",
                        },
                    )
                if path in ("/api/v1/inventory", "/inventory"):
                    if not _auth_ok(self, token):
                        return _json(self, 401, {"error": "unauthorized"})
                    return _json(
                        self,
                        200,
                        {
                            "serial": "ZY-SUITE-DA",
                            "hostname": "suite-gateway",
                            "vendor": "Zyvor",
                            "model": "suite-stub",
                        },
                    )
                if path in ("/api/v1/sensors", "/sensors"):
                    if not _auth_ok(self, token):
                        return _json(self, 401, {"error": "unauthorized"})
                    return _json(
                        self,
                        200,
                        [{"id": "cpu_temp", "value": 42.5, "unit": "C", "quality": "good"}],
                    )
                return _json(self, 404, {"error": "not found"})

            if kind == "nodra":
                if path in ("/healthz", "/readyz"):
                    return _json(self, 200, {"status": "ready", "store": "suite"})
                if not _auth_ok(self, token):
                    return _json(self, 401, {"error": "unauthorized"})
                if path == "/api/v1/devices":
                    return _json(
                        self,
                        200,
                        [
                            {
                                "id": "dev_suite_1",
                                "name": "Line PLC",
                                "site_id": "site_suite",
                                "protocol": "mqtt",
                            }
                        ],
                    )
                if path == "/api/v1/twins":
                    return _json(
                        self,
                        200,
                        [
                            {
                                "device_id": "dev_suite_1",
                                "reported": {"cpu_temp": 41.0, "heartbeat": 1},
                                "desired": {"ota": {"version": "1.2.3"}},
                            }
                        ],
                    )
                if path == "/api/v1/ota/campaigns":
                    return _json(
                        self,
                        200,
                        [
                            {
                                "id": "otacamp_suite",
                                "name": "suite-canary",
                                "status": "running",
                                "current_stage": 0,
                                "stages": [{"canary_percent": 25}, {"canary_percent": 100}],
                            }
                        ],
                    )
                return _json(self, 404, {"error": "not found"})

            if kind == "fleet":
                if path in ("/readyz", "/healthz"):
                    return _json(self, 200, {"schema": 1, "status": "ready"})
                if not _auth_ok(self, token):
                    return _json(self, 401, {"error": "unauthorized"})
                if path == "/api/v1/sites":
                    return _json(self, 200, [{"id": "site_suite", "name": "Suite Plant"}])
                if path == "/api/v1/rollouts":
                    return _json(
                        self,
                        200,
                        [{"id": "ro_suite", "name": "canary", "status": "running"}],
                    )
                if path == "/api/v1/ota/devices":
                    return _json(
                        self,
                        200,
                        [{"deviceId": "NLDW-SUITE", "name": "suite-host", "state": "idle"}],
                    )
                return _json(self, 404, {"error": "not found"})

            if kind == "yard":
                if path in ("/api/v1/health", "/healthz"):
                    return _json(self, 200, {"status": "ok"})
                return _json(self, 404, {"error": "not found"})

            return _json(self, 404, {"error": "unknown peer"})

        def do_POST(self) -> None:  # noqa: N802
            path = urlparse(self.path).path
            state.hits.append(f"POST {kind}{path}")
            if kind != "yard":
                return _json(self, 405, {"error": "method"})
            if not _auth_ok(self, token):
                return _json(self, 401, {"error": "invalid connector token"})
            body = _read_json(self)
            if path in ("/api/v1/ingest/inventory", "/api/v1/ingest/inventory/"):
                if isinstance(body, dict):
                    state.yard_inventory.append(body)
                return _json(self, 202, {"accepted": True})
            if path in ("/api/v1/ingest/observations", "/api/v1/ingest/observations/"):
                state.yard_observations.append(body)
                return _json(self, 202, {"accepted": True})
            return _json(self, 404, {"error": "not found"})

    return Handler


class Peer:
    def __init__(self, kind: str, token: str, state: PeerState) -> None:
        self.kind = kind
        self.token = token
        self.state = state
        self.httpd = ThreadingHTTPServer(
            ("127.0.0.1", 0), make_handler(kind, token, state)
        )
        self.port = self.httpd.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self._thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)

    def start(self) -> "Peer":
        self._thread.start()
        return self

    def stop(self) -> None:
        self.httpd.shutdown()
