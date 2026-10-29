#!/usr/bin/env bash
# Switch `current` back to the release that was live before the last deploy.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/common.sh"

previous_file="$PC_STATE_DIR/previous"
if [ ! -f "$previous_file" ]; then
    echo "rollback: no previous release recorded" >&2
    exit 1
fi
previous="$(cat "$previous_file")"
if [ ! -d "$previous" ]; then
    echo "rollback: previous release is missing: $previous" >&2
    exit 1
fi

failed=""
if [ -L "$PC_CURRENT_LINK" ]; then
    failed="$(readlink -f "$PC_CURRENT_LINK")"
fi
switch_to "$previous"
# A second rollback then returns to the release that was just replaced.
if [ -n "$failed" ]; then
    printf '%s\n' "$failed" > "$previous_file"
fi
echo "rolled back to: $previous"
