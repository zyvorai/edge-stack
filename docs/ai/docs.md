# AI docs (edge-stack)

_Generated 2026-10-20 by claude-opus-5-5 from a snapshot of tracked sources; verify before acting._

# Part 1: Improved README.md

```markdown
# Zyvor Edge Stack

[![Suite CI](https://github.com/zyvorai/edge-stack/actions/workflows/suite-ci.yml/badge.svg)](https://github.com/zyvorai/edge-stack/actions/workflows/suite-ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Pages](https://img.shields.io/badge/docs-GitHub%20Pages-informational)](https://zyvorai.github.io/edge-stack/)

![Zyvor Edge Stack — one map of the edge line](docs/social/edge-stack-share-card.png)

**A static landing page and a hermetic Python smoke test that checks the HTTP contracts between Zyvor edge products. It needs no product binaries.**

📖 **[Live site](https://zyvorai.github.io/edge-stack/)** · **[How they fit](docs/HOW_THEY_FIT.md)** · **[Suite CI](docs/SUITE_CI.md)**

## What this repo is (and isn't)

This repo **is**:

- `index.html`, a static GitHub Pages site about the Zyvor edge line: Device Agent, Nodra, Fleet, OTA, Yard, relay-edge and relay-pubsub.
- `scripts/suite_peers.py`, in-process HTTP stubs for Device Agent, Nodra, Fleet and a Yard ingest sink. They speak the request and response shapes that Yard's connectors use.
- `scripts/suite_smoke.py`, a smoke test. It drives those stubs through the cross-product paths and exits non-zero on any failure.
- `docs/`, the suite narrative ([HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md)) and the CI explainer ([SUITE_CI.md](docs/SUITE_CI.md)).

This repo **is not**:

- A monorepo build. Each product builds and qualifies in its own repo. Run `make help` there.
- A product qualification. A green check here means the stubbed wire shapes still agree. It does not mean any product binary works.

> **Maturity:** This repo provides integration smoke and narrative docs. Product maturity is tracked in each upstream repo.

## Contents

- [Requirements](#requirements)
- [Quick start](#quick-start)
- [What the smoke checks](#what-the-smoke-checks)
- [Configuration](#configuration)
- [CI](#ci)
- [Repository layout](#repository-layout)
- [Contributing](#contributing)
- [License](#license)

## Requirements

**Suite smoke:**

- Python 3. CI uses **3.12**.
- Standard library only (`http.server`, `urllib`, `json`, `threading`). Nothing needs to be installed with pip.
- Bash, for the wrapper script.

**Share-card rendering only (optional):**

- macOS, because the script uses `sips`.
- Google Chrome.

## Quick start

```bash
git clone https://github.com/zyvorai/edge-stack.git
cd edge-stack
./scripts/run-suite-smoke.sh
```

The wrapper does two things:

1. It byte-compiles `suite_peers.py` and `suite_smoke.py` with `python3 -m py_compile`.
2. It runs the smoke.

You can also run the smoke directly:

```bash
cd scripts && python3 suite_smoke.py
```

Run it from `scripts/`, because `suite_smoke.py` imports `suite_peers` as a sibling module.

### Output

Each check prints `PASS  <label>` to stdout or `FAIL  <label> — <detail>` to stderr. The run ends with a summary like this:

```
Suite smoke: N passed, M failed
```

The exit code is `0` only when every check passes.

The stubs bind to `127.0.0.1` on OS-assigned ephemeral ports. The run needs no network access and doesn't conflict with local services.

## What the smoke checks

| Section | Checks |
|---|---|
| **Path A: Device Agent → Yard** | <ul><li>Health endpoint responds.</li><li>`/api/v1/inventory` returns **401** without a bearer token and **200** with one.</li><li>`/api/v1/sensors` returns a non-empty list.</li><li>Yard ingest returns **202** for the normalized inventory row and for the observation batch.</li></ul> |
| **Path B: Nodra → Yard** | <ul><li>`/readyz` responds.</li><li>`/api/v1/devices` and `/api/v1/twins` are fetched, and the twin's `device_id` must match the device `id`.</li><li>`/api/v1/ota/campaigns` returns a `running` campaign.</li><li>The Nodra device is ingested into Yard as inventory.</li><li>Only **numeric** twin `reported` fields are ingested as observations.</li></ul> |
| **Path C: Fleet lifecycle** | <ul><li>`/readyz`, `/api/v1/sites`, `/api/v1/rollouts` and `/api/v1/ota/devices` respond.</li><li>A compact summary (`sites`, `rollouts_total`, `rollouts_active`, `ota_devices`) is built and checked for at least one site and at least one active rollout.</li><li>This path calls only the Fleet stub. It does not post to Yard.</li></ul> |
| **Path D: relay-pubsub contract** | <ul><li>Checks a static table of documented backends: `memory`, `http`, `relay-events`, and `grpc` (labelled a scaffold).</li><li>It starts no relay-pubsub stub and makes no HTTP calls.</li></ul> |
| **Ingest accounting** | The Yard sink must have received at least 2 inventory rows and at least 2 observation batches, from Device Agent and Nodra together. |

Section labels in the smoke differ from [HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md):

- The smoke's "Path D" is relay-pubsub.
- In HOW_THEY_FIT.md, Path D is OTA ownership and relay-pubsub is Path E.

For what the suite deliberately does **not** cover (RAUC flashing, HIL, Fleet HA, live lab hosts), see [SUITE_CI.md](docs/SUITE_CI.md#what-suite-ci-does-not-claim).

## Configuration

### Suite smoke

The suite smoke has no configuration. Stub tokens are hard-coded in `suite_smoke.py`:

| Stub | Token |
|---|---|
| Device Agent | `da-suite-token` |
| Nodra | `nodra-suite-token` |
| Fleet | `fleet-suite-token` |
| Yard ingest | `yard-ingest-token` |

Ports are ephemeral, and the HTTP timeout is 10 s per request.

Real connector settings are documented in [HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md). These include `config.auth_token`, `config.tls_insecure`, `config.source`, `YARD_URL` and lab ports. They belong to Yard and the products, not to this repo.

### Share cards (`docs/social/build-social-card.sh`)

```bash
./docs/social/build-social-card.sh [SOCIAL_OUT] [SHARE_OUT]
```

| Input | Default | Purpose |
|---|---|---|
| `CHROME` (env) | `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` | Path to the Chrome binary used for headless screenshots |
| `TMPDIR` (env) | `/tmp` | Where temporary PNGs are written |
| `$1` | `docs/social/edge-stack-social-card.jpg` | 1600×900 JPEG, rendered from `edge-stack-social-card.html` |
| `$2` | `docs/social/edge-stack-share-card.png` | 1200×630 PNG, rendered from `edge-stack-share-card.html` (used at the top of this README) |

## CI

The GitHub Actions workflow [`suite-ci`](.github/workflows/suite-ci.yml) runs on these triggers:

- every push to `main`
- every pull request
- manual dispatch (`workflow_dispatch`)

It runs on `ubuntu-latest` with Python 3.12 and a 10-minute timeout. The steps are:

1. Byte-compile `suite_peers.py` and `suite_smoke.py`.
2. Run `./scripts/run-suite-smoke.sh`.
3. Check the docs:
   - `docs/HOW_THEY_FIT.md` and `docs/SUITE_CI.md` must exist.
   - `HOW_THEY_FIT.md` must contain `Path A`.
   - `SUITE_CI.md` must mention `suite_smoke.py`.

A newer run on the same ref cancels any in-progress run.

## Repository layout

| Path | Purpose |
|---|---|
| `index.html` | Static landing page, served by GitHub Pages |
| `docs/HOW_THEY_FIT.md` | Products, repos, data paths, lab ports, ownership |
| `docs/SUITE_CI.md` | How to run and read the suite job |
| `docs/social/` | Share-card HTML sources, rendered images, `build-social-card.sh` |
| `scripts/suite_peers.py` | In-process HTTP peer stubs |
| `scripts/suite_smoke.py` | Cross-product smoke runner |
| `scripts/run-suite-smoke.sh` | Compile + run wrapper (what CI calls) |
| `.github/workflows/suite-ci.yml` | CI workflow |

## Contributing

| Change | Edit |
|---|---|
| Landing copy / layout | `index.html` |
| Suite narrative, ports, ownership | `docs/HOW_THEY_FIT.md` |
| Connector wire shapes | `scripts/suite_peers.py` **and** `scripts/suite_smoke.py` |
| Share cards | `docs/social/*.html`, then re-render with `./docs/social/build-social-card.sh` |

Follow these rules for every change:

- **Keep stubs and narrative in sync.** If a product changes a wire contract, update `scripts/suite_peers.py` and `docs/HOW_THEY_FIT.md` in the **same PR**.
- **Run the smoke before you push:** `./scripts/run-suite-smoke.sh`.
- **Don't break the docs check.** CI fails if `HOW_THEY_FIT.md` loses the string `Path A` or `SUITE_CI.md` stops mentioning `suite_smoke.py`.
- **Source the content.** Content on the landing page and in the docs should come from each product's own documentation.
- **Add a license header to new scripts.** Use `SPDX-License-Identifier: Apache-2.0`, matching the existing files.

## License

Apache-2.0. See [LICENSE](LICENSE).

Product names and quoted copy belong to their respective Zyvor projects.
```

---

# Part 2: Documentation gaps I could not fill

**`make ci` is unverifiable.** The original README and the social card both tell users to run `make ci`, but no `Makefile` was provided. I removed it from the README. Someone should confirm whether a Makefile exists and what its `ci` target runs.

**Minimum Python version is unknown.** CI pins 3.12. The code uses `from __future__ import annotations` with `str | None` and `list[...]` hints, which suggests 3.7+ might work. This hasn't been tested or stated, so I documented only "Python 3, CI uses 3.12".

**The CI trigger description was wrong.** The old README said CI runs on push and PR "to `main`". The workflow actually triggers on **all** pull requests, plus `workflow_dispatch`. I documented the actual behaviour. Maintainers should decide whether PRs should be restricted to `main`.

**Path numbering differs between the smoke and HOW_THEY_FIT.md.**
- In `suite_smoke.py`, Path D is relay-pubsub.
- In `HOW_THEY_FIT.md`, Path D is OTA and relay-pubsub is Path E.
- `SUITE_CI.md` follows the smoke's numbering.

I noted the mismatch, but the source docs should be reconciled.

**Path D is a self-referential check.** The smoke compares a hard-coded dict against a hard-coded set. It never calls relay-pubsub, and no relay-pubsub stub exists. Its docstring calls it an "HTTP stub in this smoke", which the code doesn't support. Two things need clarifying:
- whether this is intentional
- what "documented boundary" is meant to guarantee

**Path C coverage is narrower than the docs claim.**
- `HOW_THEY_FIT.md` says the summary includes rollout "paused/failed" counts. The smoke computes only `sites`, `rollouts_total`, `rollouts_active` and `ota_devices`.
- `SUITE_CI.md` describes Path C as "Fleet → Yard", but nothing is posted to Yard.

**The stubs are not checked against the real products.** Nothing shows how the stub shapes are verified against Device Agent, Nodra, Fleet or Yard. For example, there are no recorded fixtures, schema files or upstream test links. "Same HTTP shapes Yard's connectors call" is asserted, not demonstrated.

**Some contract claims have no test.**
- Fleet's `zf_api_…` token minting and the `X-Zyvor-Request: 1` header are described but never exercised.
- Device Agent HTTPS/TLS is described, but the stubs are plain HTTP.

**Some stub endpoints are never exercised.** These exist in the stubs but no smoke step calls them:
- Device Agent `/healthz` and the unversioned `/inventory` and `/sensors`
- Nodra `/healthz`
- Fleet `/healthz`
- Yard's `/api/v1/health` and `/healthz`
- the trailing-slash ingest routes

It's unclear whether these are meant to be covered.

**Failures can crash instead of reporting.** If an early hop returns an unexpected body, a later step can raise an exception (for example `KeyError` or `AttributeError` on `inv["serial"]`) instead of recording a `FAIL`. The exit code is still non-zero, but the "N passed, M failed" summary won't print. This behaviour isn't documented.

**`index.html` content was not provided.** I couldn't describe what the landing page shows or confirm the "every quote from product docs" claim.

**GitHub Pages configuration was not provided.** "Pages from `main` `/`" comes from the old README and couldn't be checked against any repo settings or workflow.

**The share-card source asset is missing.** Both card HTML files reference `zyvor-mark.svg`, which wasn't provided. I also couldn't confirm whether the rendered images are committed and kept up to date.

**Share cards can't be built on Linux or Windows.** The script hard-depends on macOS `sips`, and no alternative is documented.

**The LICENSE file was not provided.** Apache-2.0 is taken from the badge and the SPDX headers.

**There are no contribution process docs.** I found no `CONTRIBUTING.md`, code of conduct, issue or PR templates, DCO/CLA requirements, code-owner or review policy, or linting/formatting standards. The Python files contain `noqa` hints, which suggests some linter is used, but it isn't specified.

**Optional Relay and Zynera products are unexplained.** The old README mentions "optional Relay / Zynera". Zynera appears nowhere else in the provided files, so I dropped it.

**There is no versioning or release information.** Nothing explains how this repo tracks product versions or which upstream versions the stubs correspond to.
