# AI code review (edge-stack)

_Generated 2026-10-20 by claude-opus-5-5 from a snapshot of tracked sources; verify before acting._

## Summary
Edge Stack is a static GitHub Pages landing site (`index.html`, not included in what I reviewed) for the Zyvor edge products. It also holds a small "suite CI": in-process Python HTTP stubs (`scripts/suite_peers.py`) and a smoke driver (`scripts/suite_smoke.py`) that act out the HTTP shapes Yard connectors use against Device Agent, Nodra and Fleet. Docs in `docs/HOW_THEY_FIT.md` and `docs/SUITE_CI.md` tell the cross-product story.

## Bugs and correctness risks

- **The smoke mostly tests itself.**
  - `suite_peers.py` and `suite_smoke.py` are written together, and nothing ties them to the real upstream APIs (no fixtures, schemas or pinned upstream versions).
  - The Yard ingest stub accepts any body. Inventory is stored only if it is a dict; observations are stored unconditionally, including `None`.
  - So `SUITE_CI.md`'s claim that a green check means "Yard ingest still accepts the normalized inventory/observation bodies" is not demonstrated. A real upstream contract change would not turn this CI red.
- **Path D (relay-pubsub) is a tautology.**
  - `path_relay_pubsub_contract()` builds a hard-coded dict and then asserts that its keys equal the same literal set.
  - It also asserts that a string it just wrote starts with `"scaffold"`.
  - This can never fail and touches no relay-pubsub code or docs. Yet `SUITE_CI.md` lists it as a "covered" path.
- **Failures crash instead of being counted.** In `suite_smoke.py`, `require()` arguments are evaluated before the check runs. On an unexpected response, the script throws a traceback instead of reporting `FAIL`. Examples:
  - `inv.get("hostname", "")` raises `AttributeError` if `http_json` returned a string body.
  - `camps[0]["name"]`, `twins[0]["device_id"]` and `rollouts[0]["status"]` raise when the list is empty or the body is an error dict.
  - `http_json` catches only `HTTPError`. A `URLError` or `RemoteDisconnected` (for example, from a malformed-JSON POST that makes `_read_json` raise inside the handler) propagates uncaught.
  - CI still goes red, but the PASS/FAIL accounting is bypassed.
- **Weak assertions.**
  - The final ingest accounting uses `>= 2`, so duplicate or extra posts go unnoticed; `== 2` would be stricter.
  - Path A checks `len(yard_observations) >= 1` against shared state, not the batch it just posted.
  - Path C documents a summary with "rollout totals/active/paused/failed", but the smoke computes only `active` and never checks paused or failed.
- **Documented connector behaviour that is not exercised:**
  - the fallback routes `/inventory` and `/sensors`;
  - TLS and the `tls_insecure` behaviour (the stubs are plain HTTP);
  - Fleet `zf_api_…` token minting and the `X-Zyvor-Request: 1` header;
  - the Fleet `/v1/devices/...` assignment contract named in `HOW_THEY_FIT.md`.
- **Path lettering is inconsistent.**
  - `HOW_THEY_FIT.md`: D = OTA, E = relay-pubsub.
  - `SUITE_CI.md` and `suite_smoke.py`: D = relay-pubsub.
  - `HOW_THEY_FIT.md` also says Path A is covered "in `suite_smoke.py`", but there is no OTA-specific Path D there.
- **`make ci` may not exist.** It is referenced in `README.md` and the social card, but no `Makefile` appears in the reviewed files. It may have been truncated, so this needs confirming.
- **`Peer.stop()`** calls `shutdown()` but never `server_close()` or a thread join. This is a minor socket leak, harmless in a one-shot script.

## Security concerns

- **Insecure TLS default (upstream Yard, documented here).** `HOW_THEY_FIT.md` states Yard skips TLS verification on `https://` unless `config.tls_insecure` is explicitly `false`. That default is insecure. This repo only documents it, but it should at least carry a warning and ideally push upstream for secure-by-default.
- **Unpinned actions.** `actions/checkout@v4` and `actions/setup-python@v5` are referenced by tag, not commit SHA. The risk is low given `permissions: contents: read`.
- **Stubs look fine.** They bind to `127.0.0.1`, use throwaway tokens, and use non-constant-time bearer comparison. All of that is acceptable for test-only code.
- **`build-social-card.sh`** runs headless Chrome on local `file://` HTML. Risk is low.

## Test and CI gaps

- **No upstream contract source.** Nothing pulls OpenAPI specs or recorded fixtures from the product repos, and no job runs against real binaries or containers, even on a nightly schedule.
- **Redundant compile step.** `py_compile` runs twice: once in the workflow and again in `run-suite-smoke.sh`.
- **Shallow docs check.** The "Docs present" step only greps for `Path A` and `suite_smoke.py`.
- **Nothing checks the site or tooling quality:**
  - no lint or type check (ruff/mypy);
  - no link check or HTML validation for `index.html` and the docs;
  - no Mermaid render check.
- **Narrow runtime coverage.** There is a single Python version (3.12) and no stated minimum.
- **Unenforced card regeneration.** `build-social-card.sh` is macOS-only (it uses `sips` and a Chrome app path), so nothing in CI checks that the cards are regenerated.

## Documentation gaps

- The README says CI runs "on every push and pull request to `main`". In fact pushes trigger only on `main`, while PRs trigger for every target branch.
- `make ci` is undocumented or missing, as noted above.
- No doc states which upstream versions or commits the stubs reflect, or how drift is detected.
- `SUITE_CI.md` overstates what Path D and the ingest checks prove. Its "What suite CI does not claim" list should add "stubs are hand-written, not derived from upstream".
- The README does not mention that the social-card build is macOS-only.
- The README mentions "Relay / Zynera", but `HOW_THEY_FIT.md` never covers Zynera.

## Top 5 recommended actions

1. **Anchor the stubs to real contracts.** Vendor OpenAPI specs or JSON fixtures from each upstream repo, with recorded versions. Validate both stub responses and ingest bodies against them, and make the Yard sink reject malformed bodies.
2. **Replace or relabel Path D.** Either test something real (for example, parse relay-pubsub's documented backend list or run its memory backend) or label it plainly as documentation, not a passing check.
3. **Harden `suite_smoke.py`.**
   - Guard indexing and `.get` behind status checks.
   - Catch `URLError` and connection errors.
   - Tighten the counts to exact values.
   - Add the paused/failed rollout fields and the fallback routes.
4. **Fix the docs and build entry points.**
   - Align path lettering across `HOW_THEY_FIT.md`, `SUITE_CI.md` and `suite_smoke.py`.
   - Correct the trigger description.
   - Add or remove `make ci`.
   - Add a warning about Yard's insecure TLS default.
5. **Strengthen CI.**
   - Pin actions to SHAs.
   - Drop the duplicate compile step.
   - Add ruff/mypy and a link/HTML check for `index.html` and the docs.
   - Consider a scheduled job against real product containers.
