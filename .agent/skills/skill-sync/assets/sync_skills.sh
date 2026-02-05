#!/usr/bin/env bash
# Wrapper for sync_skills.py
# Usage: ./sync_skills.sh [--dry-run] [--scope <scope>]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/sync_skills.py"

# Run with python3 (or python)
if command -v python3 &>/dev/null; then
    python3 "$PYTHON_SCRIPT" "$@"
elif command -v python &>/dev/null; then
    python "$PYTHON_SCRIPT" "$@"
else
    echo "Error: Python is required to run this script."
    exit 1
fi