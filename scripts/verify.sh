#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "BLOCKED: run make setup to create the Python environment." >&2
  exit 2
fi

"$ROOT/.venv/bin/ruff" check "$ROOT/backend" "$ROOT/scripts" "$ROOT/tests"
"$PYTHON" "$ROOT/scripts/verify_baseline.py"
"$PYTHON" "$ROOT/scripts/validate_mapping_schema.py"
npm --prefix "$ROOT/frontend" run build
