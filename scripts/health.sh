#!/usr/bin/env bash
# Succeed once the live server answers the calculator API with a JSON result; retry while it starts up.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/common.sh"

for ((i = 1; i <= PC_HEALTH_RETRIES; i++)); do
    if body="$("$CURL" -fsS --max-time 10 "$PC_HEALTH_URL")" && grep -q '"rows"' <<<"$body"; then
        echo "healthy: $PC_HEALTH_URL"
        exit 0
    fi
    echo "attempt $i/$PC_HEALTH_RETRIES failed" >&2
    if ((i < PC_HEALTH_RETRIES)); then sleep "$PC_HEALTH_DELAY"; fi
done
echo "unhealthy: $PC_HEALTH_URL" >&2
exit 1
