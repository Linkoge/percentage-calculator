#!/usr/bin/env bash
# Archive the release that `current` points at, so a failed deploy can be inspected or restored by hand.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/common.sh"

mkdir -p "$PC_BACKUP_DIR"
if [ ! -L "$PC_CURRENT_LINK" ]; then
    echo "nothing to back up: no current release yet"
    exit 0
fi
archive="$PC_BACKUP_DIR/$(stamp).tar.gz"
tar -czf "$archive" -C "$(readlink -f "$PC_CURRENT_LINK")" .
echo "backup: $archive"

backups=("$PC_BACKUP_DIR"/*.tar.gz)
for ((i = 0; i < ${#backups[@]} - PC_KEEP_BACKUPS; i++)); do rm -f -- "${backups[i]}"; done
