# Shared settings for the deploy scripts; sourced, not executed.
# Every value can be overridden from the environment. Tests point these at disposable
# directories and fake systemctl/curl shims; the live host uses the defaults.
ROOT="${ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PC_HOME="${PC_HOME:-${XDG_DATA_HOME:-$HOME/.local/share}/percentage-calculator}"
PC_RELEASES_DIR="${PC_RELEASES_DIR:-$PC_HOME/releases}"
PC_CURRENT_LINK="${PC_CURRENT_LINK:-$PC_HOME/current}"
PC_BACKUP_DIR="${PC_BACKUP_DIR:-$PC_HOME/backups}"
PC_STATE_DIR="${PC_STATE_DIR:-$PC_HOME/state}"
PC_SERVICE="${PC_SERVICE:-percentage-calculator.service}"
PC_PORT="${PORT:-8090}"
PC_HEALTH_URL="${PC_HEALTH_URL:-http://127.0.0.1:$PC_PORT/api/calc?total=200&amount=50}"
PC_HEALTH_RETRIES="${PC_HEALTH_RETRIES:-10}"
PC_HEALTH_DELAY="${PC_HEALTH_DELAY:-2}"
PC_KEEP_RELEASES="${PC_KEEP_RELEASES:-5}"
PC_KEEP_BACKUPS="${PC_KEEP_BACKUPS:-20}"
SYSTEMCTL="${SYSTEMCTL:-systemctl}"
CURL="${CURL:-curl}"

stamp() { date -u +%Y%m%dT%H%M%SZ; }

# Point the `current` symlink at a release directory in one atomic rename, then restart the user service.
switch_to() {
    mkdir -p "$PC_HOME"
    local tmp_link="$PC_HOME/.current.$$"
    ln -sfn "$1" "$tmp_link"
    mv -T "$tmp_link" "$PC_CURRENT_LINK"
    "$SYSTEMCTL" --user restart "$PC_SERVICE"
}
