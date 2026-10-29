#!/usr/bin/env bash
# Copy the runtime files into a new release, switch `current` to it and restart the user service.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/common.sh"

mkdir -p "$PC_RELEASES_DIR" "$PC_STATE_DIR"
release="$PC_RELEASES_DIR/$(stamp)-$$"
mkdir "$release"
cp -a "$ROOT/server.py" "$ROOT/calc.py" "$ROOT/static" "$release/"

# Remember what was live so rollback.sh can return to it.
if [ -L "$PC_CURRENT_LINK" ]; then
    readlink -f "$PC_CURRENT_LINK" > "$PC_STATE_DIR/previous"
fi
switch_to "$release"
echo "deployed: $release"

releases=("$PC_RELEASES_DIR"/*)
for ((i = 0; i < ${#releases[@]} - PC_KEEP_RELEASES; i++)); do rm -rf -- "${releases[i]}"; done
