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

E2E_DATA_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/sdlc-qe-e2e.XXXXXX")"
cleanup() {
  rm -rf -- "$E2E_DATA_ROOT"
}
trap cleanup EXIT
export SDLC_QE_DATA_DIR="$E2E_DATA_ROOT"

if [[ -z "${E2E_FRONTEND_PORT:-}" ]]; then
  E2E_FRONTEND_PORT="$("$ROOT/.venv/bin/python" -c 'import socket; sock = socket.socket(); sock.bind(("127.0.0.1", 0)); print(sock.getsockname()[1]); sock.close()')"
fi
export E2E_FRONTEND_PORT

npm --workspace frontend run e2e
