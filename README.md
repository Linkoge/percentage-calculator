# percentage-calculator

A single-page percentage calculator. Enter a **Total (100%)**, add amount rows
(optional labels), and see each amount's share live with a progress bar, plus the
sum and the remaining amount/percentage. Handles empty, zero and invalid input,
and amounts exceeding the total. Responsive, with automatic light/dark theme.

## Run

```
python server.py            # http://0.0.0.0:8090
PORT=9000 python server.py  # custom port
```

Binds to `0.0.0.0`, so it is reachable over Tailscale at `http://<tailscale-ip>:<PORT>`.
Python 3.9+ standard library only.

## Layout

- `calc.py` – calculation logic (tested); `static/app.js` mirrors it in the browser.
- `server.py` – static file server, plus `GET /api/calc?total=..&amount=..&amount=..`.
- `static/` – HTML/CSS/JS.

## Tests

```
pip install pytest
python -m pytest -q            # all
python -m pytest -q -m smoke   # smoke only
```

## Deploy

`.linko-deploy.json` declares the deploy setup: `scripts/deploy.sh` copies `server.py`, `calc.py` and `static/`
into a new release under `~/.local/share/percentage-calculator/releases/`, switches the `current` symlink to it and
restarts the user unit `percentage-calculator.service`. `scripts/backup.sh` archives the live release first,
`scripts/health.sh` checks `/api/calc` on `PORT` (default 8090), and `scripts/rollback.sh` returns to the release
that was live before the last deploy.

The unit is not installed by the scripts. Install it once on the host:

```
cp deploy/percentage-calculator.service ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now percentage-calculator.service
```

Every path and name can be overridden with `PC_*` environment variables (see `scripts/common.sh`).
`tests/test_deploy_scripts.py` exercises all scripts against disposable directories with fake `systemctl` and
`curl` shims; it never touches the real service.
