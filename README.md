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
