from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from typing import Literal


@dataclass
class ToolResult:
    tool: str
    status: Literal["pass", "fail", "error"]
    command: str
    exit_code: int
    stdout_tail: str
    stderr_tail: str


def _tail(s: str, n: int = 800) -> str:
    s = s or ""
    return s[-n:]


def tool_run_tests() -> ToolResult:
    """
    Single tool for L1: run the repo's tests.
    """
    cmd = [sys.executable, "-m", "pytest", "-q"]
    p = subprocess.run(cmd, capture_output=True, text=True, check=False)

    status: Literal["pass", "fail"] = "pass" if p.returncode == 0 else "fail"
    return ToolResult(
        tool="run_tests",
        status=status,
        command=" ".join(cmd),
        exit_code=p.returncode,
        stdout_tail=_tail(p.stdout),
        stderr_tail=_tail(p.stderr),
    )


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    # Deterministic mode for early ladder stability (no keys, no API calls).
    if "--dry-run" in argv:
        sample = ToolResult(
            tool="run_tests",
            status="pass",
            command=f"{sys.executable} -m pytest -q",
            exit_code=0,
            stdout_tail="4 passed",
            stderr_tail="",
        )
        print(json.dumps(asdict(sample), indent=2, sort_keys=True))
        return 0

    if not argv:
        print("usage: python -m agent_lab.l1_agent [--dry-run] run-tests", file=sys.stderr)
        return 2

    cmd = argv[0]
    if cmd == "run-tests":
        # Fast deterministic mode for unit tests (avoid nested pytest runs).
        if "--selftest" in argv:
            sample = ToolResult(
                tool="run_tests",
                status="pass",
                command=f"{sys.executable} -m pytest -q",
                exit_code=0,
                stdout_tail="selftest: pass",
                stderr_tail="",
            )
            print(json.dumps(asdict(sample), indent=2, sort_keys=True))
            return 0

        res = tool_run_tests()
        print(json.dumps(asdict(res), indent=2, sort_keys=True))
        return 0 if res.exit_code == 0 else 1

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
