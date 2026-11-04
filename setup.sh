#!/usr/bin/env bash
set -euo pipefail

echo "==> Verifying system dependencies..."
REQUIRED_TOOLS=("git" "ruby" "bundle")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" >/dev/null 2>&1; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -gt 0 ]; then
    echo "[ERROR] Missing required dependencies: ${MISSING_TOOLS[*]}" >&2
    echo "Please install them before continuing." >&2
    exit 1
fi

echo "==> Setting up local Ruby environment..."
bundle config set --local path 'vendor/bundle'
bundle install

echo ""
echo "Setup complete. Start the local Jekyll server with:"
echo "  bundle exec jekyll serve --baseurl \"\""
