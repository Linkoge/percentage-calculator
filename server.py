"""Tiny static server for the percentage calculator."""
from __future__ import annotations

import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import calc

STATIC = Path(__file__).parent / "static"


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/calc":
            q = parse_qs(url.query)
            body = json.dumps(calc.summarize(
                (q.get("total") or [""])[0], q.get("amount", []))).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        if os.environ.get("QUIET"):
            return
        super().log_message(fmt, *args)


def make_server(host: str = "0.0.0.0", port: int = 47613) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), partial(Handler, directory=str(STATIC)))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "47613"))
    srv = make_server("0.0.0.0", port)
    print(f"Serving on http://0.0.0.0:{port}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
