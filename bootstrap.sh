#!/usr/bin/env bash
set -euo pipefail

# bootstrap.sh
# Purpose: recreate the L0 repo scaffold deterministically.
# Safe to re-run: it overwrites the known baseline files.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

mkdir -p docs/work_orders src/agent_lab tests .github/workflows runs
: > runs/.gitkeep

cat > README.md <<'EOF'
# codex-agent-swarm-lab

A ladder repo for building trustworthy, repeatable agent workflows ("swarms") the boring way:
verifiable outputs, tests, CI gates, and run logs.

Quickstart (L0)

  python -m venv .venv
  source .venv/Scripts/activate
  python -m pip install -U pip
  python -m pip install -e ".[dev]"
  python -m pytest -q

  agent-lab hello Nick
  python -m agent_lab hello Nick
EOF

cat > docs/LEVELS.md <<'EOF'
# Levels (Swarm Ladder)

## L0 — Deterministic CLI + tests + CI (NOW)
Goal: baseline repo that proves we can ship changes with a green check.

Acceptance:
- `pytest` passes locally
- GitHub Actions CI passes
- CLI output is deterministic

## L1 — Single Agent + One Tool Call
Goal: learn “agent + tool” fundamentals (schemas, tool invocation, validation).

## L2 — Structured Outputs + Validation + Run Artifacts
Goal: structured outputs (JSON), validation, and replayable evidence.
Deliverable: `runs/<timestamp>/...`

## L3 — Multi-Agent Handoffs (2–3 agents)
Planner → Implementer → Tester, with acceptance checks.

## L4 — Guardrails + Tracing
Approvals for risky actions + tracing of tool calls/handoffs.

## L5 — Swarm Orchestration + Evals
Eval suite: pass rate, loop count, tool error rate, cost/run.
EOF

cat > docs/work_orders/L0.md <<'EOF'
# Work Order — L0: Deterministic CLI + Tests + CI

## Acceptance Criteria
- `agent-lab --help` exits 0
- `agent-lab --version` prints a version string
- `agent-lab hello Nick` prints: `hello Nick`
- `python -m agent_lab hello Nick` prints: `hello Nick`
- `pytest` passes locally
- CI passes on GitHub Actions
EOF

cat > AGENTS.md <<'EOF'
# Agent Contract (Human + AI)

Each change must be verifiable.

Roles:
- Planner: spec + acceptance only
- Implementer: code only
- Tester: tests only
- Reviewer: risks + checklist

Rule:
If it can’t be verified, it doesn’t ship.
EOF

cat > .env.example <<'EOF'
OPENAI_API_KEY=
EOF

cat > src/agent_lab/__init__.py <<'EOF'
__all__ = ["__version__"]
__version__ = "0.1.0"
EOF

cat > src/agent_lab/__main__.py <<'EOF'
from agent_lab.cli import main

raise SystemExit(main())
EOF

cat > src/agent_lab/cli.py <<'EOF'
from __future__ import annotations

import argparse

from agent_lab import __version__


def _maybe_load_dotenv() -> None:
    """Optional: establish the .env convention early without making it a hard dependency."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except Exception:
        return
    load_dotenv()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="agent-lab", description="Swarm ladder CLI (L0).")
    p.add_argument("--version", action="store_true", help="Print version and exit.")
    sub = p.add_subparsers(dest="cmd", required=False)

    hello = sub.add_parser("hello", help="Say hello deterministically.")
    hello.add_argument("name", nargs="?", default="world")
    return p


def main(argv: list[str] | None = None) -> int:
    _maybe_load_dotenv()
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        print(__version__)
        return 0

    if args.cmd == "hello":
        print(f"hello {args.name}")
        return 0

    parser.print_help()
    return 0
EOF

cat > tests/test_cli.py <<'EOF'
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
EOF

cat > pyproject.toml <<'EOF'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "codex-agent-swarm-lab"
version = "0.1.0"
description = "A ladder repo for verifiable agent swarms."
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "ruff>=0.5.0"]
agents = ["openai>=1.0.0", "python-dotenv>=1.0.0"]

[project.scripts]
agent-lab = "agent_lab.cli:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
EOF

cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.pytest_cache/
dist/
build/
*.egg-info/
.env
EOF

cat > .gitattributes <<'EOF'
* text=auto eol=lf
EOF

cat > Makefile <<'EOF'
.PHONY: install test lint fmt run

install:
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

test:
	python -m pytest -q

lint:
	python -m ruff check .
	python -m ruff format --check .

fmt:
	python -m ruff check . --fix
	python -m ruff format .

run:
	python -m agent_lab --help
EOF

cat > .github/workflows/ci.yml <<'EOF'
name: ci

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install
        run: |
          python -m pip install -U pip
          pip install -e ".[dev]"
      - name: Lint
        run: |
          ruff check .
          ruff format --check .
      - name: Test
        run: pytest -q
EOF

cat > LICENSE <<'EOF'
MIT License

Copyright (c) 2026 IT Pro Direct

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
EOF

chmod +x bootstrap.sh

if [[ "${1:-}" == "--verify" ]]; then
  python -m pip install -U pip >/dev/null
  python -m pip install -e ".[dev]" >/dev/null
  python -m ruff check .
  python -m ruff format --check .
  python -m pytest -q
  python -m agent_lab hello Nick | grep -qx "hello Nick"
  echo "verify: OK"
fi

echo "bootstrap complete"
