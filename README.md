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
