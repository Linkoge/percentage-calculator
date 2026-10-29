import json
import threading
import urllib.request

import pytest

import server


@pytest.fixture
def base():
    srv = server.make_server("127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}"
    srv.shutdown()
    srv.server_close()


@pytest.mark.smoke
def test_serves_page(base):
    with urllib.request.urlopen(base + "/", timeout=10) as r:
        html = r.read().decode()
    assert r.status == 200
    assert "Total (100%)" in html


def test_serves_assets(base):
    for p in ("/style.css", "/app.js"):
        with urllib.request.urlopen(base + p, timeout=10) as r:
            assert r.status == 200


def test_api(base):
    with urllib.request.urlopen(base + "/api/calc?total=200&amount=50", timeout=10) as r:
        data = json.load(r)
    assert data["rows"][0]["percent"] == 25
