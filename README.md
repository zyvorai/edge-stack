# The Zyvor Edge Stack

**Live:** https://zyvorai.github.io/edge-stack/

A landing page for the eight-product Zyvor edge line — **Zyvor Device
Agent**, **Nodra**, **Zyvor Fleet**, **Zyvor OTA**, **relay-edge**,
**relay-pubsub**, **Zyvor Relay**, and **Zynera** — ordered as the real
systems story they tell together: hardware discovery → offline-first
runtime → fleet control plane → OS updates → event
simulation/bridging → the durable reliability loop → the optional
AI/GPU brain.

Every quote, version tag, and stat on the page is pulled directly from
each product's own README/docs — nothing invented. The two architecture
diagrams (Device Agent, OTA) are each product's own, inlined as-is.
relay-edge's screenshot is a real `/ui` capture, not a mockup.

## Structure

This is a single self-contained static file — no build step, no
dependencies beyond two Google Fonts requests (the rest is inline
CSS/SVG and a base64-embedded screenshot).

- `index.html` — the entire site.

## Updating

Edit `index.html` directly, commit, and push to `main` — GitHub Pages
redeploys automatically (Settings → Pages → Deploy from branch: `main`,
`/ (root)`).

## License

Apache-2.0 — see [LICENSE](LICENSE). Product names, marks, and quoted
copy belong to their respective Zyvor projects; this repo just presents
them together.
