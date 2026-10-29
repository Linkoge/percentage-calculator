import json
import os
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
TIMEOUT = 60

FAKE_SYSTEMCTL = """#!/bin/sh
echo "systemctl $*" >> "$FAKE_LOG"
exit "${FAKE_SYSTEMCTL_STATUS:-0}"
"""

FAKE_CURL = """#!/bin/sh
echo "curl $*" >> "$FAKE_LOG"
if [ -n "${FAKE_CURL_FAIL:-}" ]; then exit 22; fi
echo '{"rows": [{"percent": 25}]}'
"""


@pytest.fixture
def env(tmp_path):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for name, body in (("systemctl", FAKE_SYSTEMCTL), ("curl", FAKE_CURL)):
        shim = bin_dir / name
        shim.write_text(body)
        shim.chmod(0o755)
    home = tmp_path / "home"
    values = {
        "PATH": f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
        "PC_HOME": str(home / "pc"),
        "PC_HEALTH_DELAY": "0",
        "PC_HEALTH_RETRIES": "2",
        "PC_SERVICE": "test-calc.service",
        "SYSTEMCTL": str(bin_dir / "systemctl"),
        "CURL": str(bin_dir / "curl"),
        "FAKE_LOG": str(tmp_path / "calls.log"),
        "HOME": str(home),
    }
    return {**os.environ, **values}


def run(script, env, **extra):
    return subprocess.run(
        ["bash", str(SCRIPTS / script)],
        cwd=ROOT, env={**env, **extra}, capture_output=True, text=True, timeout=TIMEOUT,
    )


def current(env):
    return Path(env["PC_HOME"], "current").resolve()


def test_first_deploy_then_redeploy_and_rollback(env):
    assert run("backup.sh", env).returncode == 0
    assert run("deploy.sh", env).returncode == 0
    first = current(env)
    assert (first / "server.py").is_file() and (first / "static" / "app.js").is_file()

    assert run("backup.sh", env).returncode == 0
    assert list(Path(env["PC_HOME"], "backups").glob("*.tar.gz"))

    assert run("deploy.sh", env).returncode == 0
    second = current(env)
    assert second != first

    rolled = run("rollback.sh", env)
    assert rolled.returncode == 0, rolled.stderr
    assert current(env) == first
    calls = Path(env["FAKE_LOG"]).read_text()
    assert calls.count("systemctl --user restart test-calc.service") == 3


def test_rollback_without_previous_release_fails(env):
    run("deploy.sh", env)
    result = run("rollback.sh", env)
    assert result.returncode != 0
    assert "no previous release" in result.stderr


def test_backup_without_current_release_is_noop(env):
    result = run("backup.sh", env)
    assert result.returncode == 0
    assert "nothing to back up" in result.stdout


def test_health_passes_against_fake_curl(env):
    result = run("health.sh", env)
    assert result.returncode == 0, result.stderr
    assert "healthy" in result.stdout


def test_health_fails_after_retries(env):
    result = run("health.sh", env, FAKE_CURL_FAIL="1")
    assert result.returncode == 1
    assert "unhealthy" in result.stderr
    assert Path(env["FAKE_LOG"]).read_text().count("curl ") == 2


def test_deploy_prunes_old_releases(env):
    for _ in range(3):
        assert run("deploy.sh", env, PC_KEEP_RELEASES="2").returncode == 0
    releases = list(Path(env["PC_HOME"], "releases").iterdir())
    assert len(releases) == 2
    assert current(env) in {p.resolve() for p in releases}


def test_deploy_file_is_valid_and_points_at_existing_scripts():
    setup = json.loads((ROOT / ".linko-deploy.json").read_text())
    assert set(setup) == {"deploy_command", "backup_command", "health_command", "rollback_command"}
    for field in setup:
        argv = setup[field]
        assert isinstance(argv, list) and argv and all(isinstance(a, str) and a for a in argv)
        script = ROOT / argv[0]
        assert script.is_file() and os.access(script, os.X_OK), argv
    assert "://" not in json.dumps(setup)


@pytest.mark.smoke
def test_deploy_scripts_have_valid_syntax():
    for script in SCRIPTS.glob("*.sh"):
        result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True, timeout=TIMEOUT)
        assert result.returncode == 0, result.stderr
