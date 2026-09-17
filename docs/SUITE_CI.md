---
hero:
  eyebrow: SUITE CI
  title: Cross-product suite continuous integration
---

## Why this exists

Each Zyvor edge product has its own green CI. Users still ask: **how do they
work together?** This repository's `suite-ci` workflow answers that on every
push by exercising the **real HTTP contracts** Yard and ops tooling use
between Device Agent, Nodra, Fleet, Yard ingest, and the relay-pubsub backend
menu — without building six language toolchains on every PR.

## What runs

```bash
./scripts/run-suite-smoke.sh
# or: cd scripts && python3 suite_smoke.py
```

| Step | Script | Meaning |
|---|---|---|
| 1 | `suite_peers.py` | In-process stubs: Device Agent, Nodra, Fleet, Yard ingest sink |
| 2 | `suite_smoke.py` | Four paths (A–D) + ingest accounting; exit ≠ 0 on any failure |
| 3 | GitHub Actions `suite-ci` | `python3 -m py_compile` + smoke on `ubuntu-latest` |

## Paths covered

| Path | Proof |
|---|---|
| **A** Device Agent → Yard | Bearer gate, inventory/sensors pull, ingest 202 |
| **B** Nodra → Yard | Devices + twins join, OTA campaign list, numeric observations ingest |
| **C** Fleet → Yard | Sites, rollouts, OTA devices → lifecycle summary shape |
| **D** relay-pubsub | Documented backends including honest `grpc` scaffold |

Details and diagrams: [HOW_THEY_FIT.md](HOW_THEY_FIT.md).

## What suite CI does **not** claim

- Full binary builds of every product (see each repo's CI)
- RAUC flash / Minewing silicon HIL (see zyvor-ota)
- Multi-writer Fleet HA (design-only; soak-short is single-writer)
- Live lab hosts (optional follow-up; this job is hermetic)

## Reading a green check

A green **Suite CI** check on
[zyvorai/edge-stack](https://github.com/zyvorai/edge-stack/actions) means:

1. The connector-facing URLs and auth headers still match what Yard expects.
2. Nodra campaign list and Fleet rollout summary shapes still parse.
3. Yard ingest still accepts the normalized inventory/observation bodies the
   suite posts (same routes the connectors use).

When a product changes a wire contract, update the stubs in
`scripts/suite_peers.py` **and** the narrative in `docs/HOW_THEY_FIT.md` in the
same PR so the suite stays the source of truth for “how they fit.”
