# Copyright 2026 Zyvor AI Labs · https://zyvor.dev
# SPDX-License-Identifier: Apache-2.0
#
# Product builds live in each repo (fleet, nodra, zyvor-ota,
# zyvor-device-agent, yard, relay-edge, relay-pubsub, zorvia).
# This Makefile only runs the cross-product contract checks.

.PHONY: help suite-smoke docs-check ci

help: ## Show targets
	@grep -E '^[a-zA-Z0-9_-]+:.*## ' $(MAKEFILE_LIST) | sort | awk -F':.*## ' '{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

suite-smoke: ## Run the four connector-path smokes
	./scripts/run-suite-smoke.sh

docs-check: ## Required suite docs are present
	test -f docs/HOW_THEY_FIT.md
	test -f docs/SUITE_CI.md

ci: suite-smoke docs-check ## Same checks as suite CI
