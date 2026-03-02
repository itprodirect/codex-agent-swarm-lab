import json
import subprocess
import sys


def run_mod(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "agent_lab.l1_agent", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_dry_run_returns_json():
    p = run_mod("--dry-run")
    assert p.returncode == 0
    data = json.loads(p.stdout)

    for key in ["tool", "status", "command", "exit_code", "stdout_tail", "stderr_tail"]:
        assert key in data

    assert data["tool"] == "run_tests"
    assert data["status"] in ["pass", "fail", "error"]
    assert isinstance(data["exit_code"], int)


def test_run_tests_command_runs_and_returns_json():
    p = run_mod("run-tests", "--selftest")
    # This command should run pytest -q; allow 0 or 1 depending on repo state,
    # but output must be valid JSON either way.
    data = json.loads(p.stdout)
    assert data["tool"] == "run_tests"
    assert "pytest" in data["command"]
    assert isinstance(data["exit_code"], int)
