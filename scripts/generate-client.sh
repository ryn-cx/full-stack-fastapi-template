#! /usr/bin/env bash

set -e
set -x

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT/backend"
uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > "$PROJECT_ROOT/openapi.json"
mv "$PROJECT_ROOT/openapi.json" "$PROJECT_ROOT/frontend/"
cd "$PROJECT_ROOT/frontend"
npm run generate-client
