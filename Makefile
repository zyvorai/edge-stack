# Copyright 2026 Zyvor AI Labs · https://zyvor.dev
# SPDX-License-Identifier: Apache-2.0

.PHONY: suite-smoke docs-check

suite-smoke:
	./scripts/run-suite-smoke.sh

docs-check:
	test -f docs/HOW_THEY_FIT.md
	test -f docs/SUITE_CI.md
