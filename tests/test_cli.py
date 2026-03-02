import subprocess
import sys


def run_cmd(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "agent_lab", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_help_exits_zero():
    p = run_cmd("--help")
    assert p.returncode == 0
    assert "Swarm ladder CLI" in p.stdout


def test_version():
    p = run_cmd("--version")
    assert p.returncode == 0
    assert p.stdout.strip()


def test_hello_default():
    p = run_cmd("hello")
    assert p.returncode == 0
    assert p.stdout.strip() == "hello world"


def test_hello_name():
    p = run_cmd("hello", "Nick")
    assert p.returncode == 0
    assert p.stdout.strip() == "hello Nick"
