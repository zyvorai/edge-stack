<div align="center">

# Zyvor Edge Stack

[![Suite CI](https://github.com/zyvorai/edge-stack/actions/workflows/suite-ci.yml/badge.svg)](https://github.com/zyvorai/edge-stack/actions/workflows/suite-ci.yml)
[![License: Zyvor Production 1.0](https://img.shields.io/badge/License-Zyvor_Production_1.0-1d1d1f.svg)](LICENSE)
[![Pages](https://img.shields.io/badge/docs-GitHub%20Pages-informational)](https://zyvorai.github.io/edge-stack/)
[![Python](https://img.shields.io/badge/Python-3%20stdlib-3776AB?logo=python&logoColor=white)](scripts)

[![Book a demo](https://img.shields.io/badge/Book_a_demo-0071e3?style=for-the-badge)](https://zyvor.dev/schedule?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_hero)
[![30-day PoC](https://img.shields.io/badge/30--day_PoC-000000?style=for-the-badge)](https://zyvor.dev/poc?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_hero)
[![Quickstart](https://img.shields.io/badge/Quickstart_make_ci-409cff?style=for-the-badge)](#quickstart)

![Zyvor Edge Stack — one map of the edge line](docs/social/edge-stack-hero-dark.jpg)

### Seven edge products. One map. One smoke test.

**One map of the Zyvor edge line — landing page and suite CI.** Device Agent, Nodra, Fleet, OTA, Yard, relay-edge and relay-pubsub, with hermetic Python stubs that prove the cross-product HTTP wire shapes Yard's connectors rely on, on every push.

**7 edge products** · **4 connector paths** · **21 contract checks** · **Python stdlib only** · **Every quote from the product's own docs**

📖 **[Live site](https://zyvorai.github.io/edge-stack/)** · **[How they fit](docs/HOW_THEY_FIT.md)** · **[Suite CI](docs/SUITE_CI.md)**

</div>

---

This repository is **not** a monorepo build. It hosts the static GitHub Pages landing for Device Agent, Nodra, Fleet, OTA, Yard, relay-edge, relay-pubsub (and optional Relay / Zynera), plus hermetic Python stubs that prove cross-product HTTP wire shapes Yard connectors rely on. Every quote and diagram on the page comes from each product's own docs.


## Why Zyvor Edge Stack

| When this happens… | Zyvor Edge Stack gives you… |
|---|---|
| Every edge product has a green CI, and you still ask how they work together | One map ([HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md)): what each product owns, the data paths between them, lab ports and ownership |
| A product changes a wire contract and the ops console quietly stops syncing | `suite-ci` exercises the HTTP contracts Yard's connectors call, on every push to `main` and every pull request |
| Proving integration means building six language toolchains | Hermetic in-process stubs for Device Agent, Nodra, Fleet and a Yard ingest sink, in plain Python |
| Nobody is sure which product owns OTA, rollouts or twins | An ownership table per path: OTA owns signed RAUC installs, Fleet the device assignment contract, Nodra the canary campaigns, Yard the display |
| A suite test claims more than it proves | A written list of what suite CI does **not** claim: full builds, RAUC flashing, Fleet HA, live lab hosts |
| You need a single page to show the edge line | A static GitHub Pages site where every quote and diagram comes from each product's own docs |

![Capabilities at a glance: Box, Site, Ops, Suite CI](docs/ux/readme-capabilities.jpg)

---

## How it fits together

![Each product owns its plane; Yard pulls](docs/ux/readme-how-it-works.jpg)

Read first:

- **[docs/HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md)** — architecture, data paths, lab ports, ownership
- **[docs/SUITE_CI.md](docs/SUITE_CI.md)** — what the cross-product CI proves

Product builds stay in each repo's Makefile (`make help` there).

| Path | What suite CI proves |
|---|---|
| **A** Device Agent → Yard | Bearer gate, inventory/sensors pull, ingest 202 |
| **B** Nodra → Yard | Devices + twins join, OTA campaign list, numeric observations ingest |
| **C** Fleet → Yard | Sites, rollouts, OTA devices → lifecycle summary shape |
| **D** relay-pubsub | Documented backends including honest `grpc` scaffold |

Yard never replaces Nodra, Fleet, or OTA. It **pulls** what those planes already own and shows it as assets, observations, and integration status.

---

## Quickstart

Needs Python 3 (standard library only) and `make`.

```bash
make ci
./scripts/run-suite-smoke.sh
```

`make ci` runs the four connector-path smokes and checks that the suite docs are present; it ends with `Suite smoke: 21 passed, 0 failed`.

## Suite CI

GitHub Actions workflow **`suite-ci`** runs that smoke on every push to `main` and on every pull request. Hermetic stubs in `scripts/suite_peers.py` and `scripts/suite_smoke.py` speak the same HTTP shapes Yard's connectors call.

## Landing page

- **`site/`** — the static landing page (no dependencies, light and dark), deployed by `.github/workflows/pages.yml`. GitHub Pages must use Source = GitHub Actions for it to go live.
- **`index.html`** — the previous single-file landing page, kept unchanged (served only while Pages still uses `main` `/`).

## Updating this repo

| Change | Where |
|---|---|
| Marketing copy / layout | `site/index.html`, `site/site.css` |
| Suite narrative / ports / ownership | `docs/HOW_THEY_FIT.md` |
| Connector wire shapes | `scripts/suite_peers.py` + `scripts/suite_smoke.py` |
| Share cards | `docs/social/` — `./docs/social/build-social-card.sh` |

---

## Maturity

> **Maturity (honest):** Integration smoke and narrative docs — product maturity lives in each upstream repo. `make ci` here validates suite contracts, not full product qualification.

---

## Part of the Zyvor stack

| Product | Role in the edge line |
|---|---|
| **[Device Agent](https://github.com/zyvorai/zyvor-device-agent)** | Discover the box; local inventory/sensors; publish northbound |
| **[Nodra](https://github.com/zyvorai/nodra)** | Edge data plane — MQTT/HTTP ingest, twins, industrial connectors, staged OTA campaigns |
| **[Fleet](https://github.com/zyvorai/zyvorai-fleet)** · **[OTA](https://github.com/zyvorai/ota)** | Site control plane and rollouts · signed RAUC A/B OS updates |
| **[Yard](https://github.com/zyvorai/yard)** | Asset / ops surface — optional connectors pull peers into one console |
| **[relay-edge](https://github.com/zyvorai/relay-edge)** · **[relay-pubsub](https://github.com/zyvorai/relay-pubsub)** | Site event simulators · Google Pub/Sub–compatible gateway into Zyvor Relay |

→ [zyvor.dev](https://zyvor.dev)

---

## Support

A commercial license is required to run it (sales@zyvor.dev); a 30-day trial key is how to evaluate. If it helps you, you can donate any amount you like: <https://rzp.io/rzp/utwdYh3>. A donation is voluntary and supports development and maintenance. It is not a purchase: it buys no support, SLA, features, priority or license, and it is not tax-deductible (Zyvor AI Labs Private Limited is a company, not a charity). Support contracts are separate: [sales@zyvor.dev](mailto:sales@zyvor.dev).

---

## License and support

Zyvor Edge Stack is source-available under the **[Zyvor Production License v1.0](LICENSE)** (SPDX `LicenseRef-Zyvor-Production-1.0`, also in [LICENSES/](LICENSES/LicenseRef-Zyvor-Production-1.0.txt); see [NOTICE](NOTICE)). Evaluation (evaluation, development, testing, research, education) is free for 30 days per organization. Production use requires a commercial license from Zyvor AI Labs Private Limited ([sales@zyvor.dev](mailto:sales@zyvor.dev), [zyvor.dev/buy](https://zyvor.dev/buy)); a 30-day trial key is available for production evaluation.

**Zyvor Enterprise** adds what production teams ask for: supported releases, deployment and upgrade guidance, priority incident triage, a named technical contact and 24x7 critical intake. [Pricing](https://zyvor.dev/pricing?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_license) · [Buy / get a quote](https://zyvor.dev/buy) · [sales@zyvor.dev](mailto:sales@zyvor.dev).

Prices: INR incl. 18% GST in India; US dollars excl. tax elsewhere (VAT, GST or sales tax added where applicable). Edge support is per managed device per year: 1-999 devices USD 18 (INR 1,784), 1,000-9,999 USD 12 (INR 1,189), 10,000+ USD 8 (INR 793), annual minimum USD 5,000 (INR 495,600). A 30-day trial key is available; non-production use of the software stays free under the Zyvor Production License v1.0. Buy / get a quote: [zyvor.dev/buy](https://zyvor.dev/buy). Orders of USD 5,000 or more and quotes are invoiced in USD through Skydo. Custom pricing: contact [sales@zyvor.dev](mailto:sales@zyvor.dev).

---

<div align="center">

### Put the whole Zyvor edge line on your bench

[![Book a demo](https://img.shields.io/badge/Book_a_demo-0071e3?style=for-the-badge)](https://zyvor.dev/schedule?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_footer)
[![30-day PoC](https://img.shields.io/badge/Start_a_30--day_PoC-000000?style=for-the-badge)](https://zyvor.dev/poc?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_footer)
[![Pricing](https://img.shields.io/badge/Pricing-1d1d1f?style=for-the-badge)](https://zyvor.dev/pricing?utm_source=github&utm_medium=edge-stack&utm_campaign=readme_footer)
[![Contact sales](https://img.shields.io/badge/Contact_sales-2997ff?style=for-the-badge)](mailto:sales@zyvor.dev?subject=Zyvor%20Edge%20Stack)
[![Star on GitHub](https://img.shields.io/github/stars/zyvorai/edge-stack?style=for-the-badge&logo=github&label=Star&color=2997ff)](https://github.com/zyvorai/edge-stack)

</div>
