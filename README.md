# The Zyvor Edge Stack

**Live:** https://zyvorai.github.io/edge-stack/

Landing page **and suite CI** for the Zyvor edge line — Device Agent, Nodra,
Fleet, OTA, **Yard**, relay-edge, relay-pubsub (and optional Relay / Zynera).

**Live pages:** https://zyvorai.github.io/edge-stack/

## How the products work together

Read this first:

- **[docs/HOW_THEY_FIT.md](docs/HOW_THEY_FIT.md)** — architecture, data paths,
  lab ports, what each repo owns
- **[docs/SUITE_CI.md](docs/SUITE_CI.md)** — what the cross-product CI proves

```bash
./scripts/run-suite-smoke.sh
```

Hermetic Python stubs speak the same HTTP shapes Yard’s connectors call.
GitHub Actions workflow **`suite-ci`** runs that smoke on every push/PR.

## Landing page

- `index.html` — static marketing/docs site (GitHub Pages from `main` `/`).

Every quote and diagram on the page is taken from each product’s own docs.

## Updating

| Change | Where |
|---|---|
| Marketing copy / layout | `index.html` |
| Suite narrative / ports / ownership | `docs/HOW_THEY_FIT.md` |
| Connector wire shapes | `scripts/suite_peers.py` + `scripts/suite_smoke.py` |

## License

Apache-2.0 — see [LICENSE](LICENSE). Product names and quoted copy belong to
their respective Zyvor projects.
