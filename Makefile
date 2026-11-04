.PHONY: setup dev verify e2e

setup:
	python3.12 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -e '.[dev]'
	npm ci

dev:
	./.venv/bin/python scripts/dev.py

verify:
	./scripts/verify.sh

e2e:
	./scripts/e2e-run.sh
