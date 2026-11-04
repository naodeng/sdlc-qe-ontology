#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  echo "BLOCKED: run make setup to create the Python environment." >&2
  exit 2
fi
if [[ ! -x "$ROOT/node_modules/.bin/playwright" ]]; then
  echo "BLOCKED: run make setup to install Playwright." >&2
  exit 2
fi

npm --workspace frontend run e2e
