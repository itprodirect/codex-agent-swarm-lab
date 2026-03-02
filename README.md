# codex-agent-swarm-lab

**Build trustworthy AI agent workflows -- the boring way.**

[![CI](https://github.com/itprodirect/codex-agent-swarm-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/itprodirect/codex-agent-swarm-lab/actions/workflows/ci.yml)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A progressive ladder repo for building verifiable, repeatable agent swarms.
Each level adds exactly one capability -- deterministic CLI, single-agent tool
calls, structured outputs, multi-agent handoffs, guardrails, and finally full
swarm orchestration -- with tests and CI gates at every step.

> **Current status:** Levels 0 and 1 complete. This project is intentionally
> early-stage; the ladder is the point.

---

## Table of Contents

- [Philosophy](#philosophy)
- [Swarm Ladder Roadmap](#swarm-ladder-roadmap)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Development](#development)
- [How the Ladder Works](#how-the-ladder-works)
- [Agent Contract](#agent-contract)
- [Contributing](#contributing)
- [License](#license)

---

## Philosophy

Most agent demos skip the foundations: no tests, no CI, no structured output,
no way to verify that what shipped actually works. This repo takes the opposite
approach.

| Principle | In practice |
|---|---|
| **If it can't be verified, it doesn't ship** | Every level has acceptance criteria checked by CI |
| **Zero runtime dependencies** | stdlib only at the core; `openai` / `dotenv` are optional extras |
| **Determinism first** | `--dry-run` and `--selftest` modes produce repeatable output without API keys |
| **Progressive complexity** | Each level adds exactly one new concept |

---

## Swarm Ladder Roadmap

| Level | Capability | Status |
|:---:|---|:---:|
| **L0** | Deterministic CLI + Tests + CI | Done |
| **L1** | Single Agent + One Tool Call (structured JSON) | Done |
| **L2** | Structured Outputs + Validation + Run Artifacts | Planned |
| **L3** | Multi-Agent Handoffs (Planner / Implementer / Tester) | Planned |
| **L4** | Guardrails + Tracing | Planned |
| **L5** | Swarm Orchestration + Evals | Planned |

See [`docs/LEVELS.md`](docs/LEVELS.md) for detailed goals and
[`docs/work_orders/`](docs/work_orders/) for per-level acceptance criteria.

---

## Quick Start

**Prerequisites:** Python 3.10 or newer.

```bash
# Clone and set up
git clone https://github.com/itprodirect/codex-agent-swarm-lab.git
cd codex-agent-swarm-lab
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### L0 -- Deterministic CLI

```bash
agent-lab hello Nick
# => hello Nick

python -m agent_lab hello Nick
# => hello Nick

agent-lab --version
# => 0.1.0
```

### L1 -- Single Agent Tool Call

```bash
# Deterministic dry-run (no API key needed)
python -m agent_lab.l1_agent --dry-run
```

```json
{
  "command": "...python -m pytest -q",
  "exit_code": 0,
  "status": "pass",
  "stderr_tail": "",
  "stdout_tail": "4 passed",
  "tool": "run_tests"
}
```

```bash
# Actually run the test suite and get structured JSON output
python -m agent_lab.l1_agent run-tests
```

---

## Project Structure

```
codex-agent-swarm-lab/
├── src/agent_lab/
│   ├── __init__.py          # Package version (0.1.0)
│   ├── __main__.py          # python -m agent_lab entry point
│   ├── cli.py               # L0 deterministic CLI
│   └── l1_agent.py          # L1 agent with ToolResult dataclass
├── tests/
│   ├── test_cli.py          # L0 CLI tests
│   └── test_l1_agent.py     # L1 agent tests
├── docs/
│   ├── LEVELS.md            # Swarm ladder roadmap
│   └── work_orders/
│       ├── L0.md            # L0 acceptance criteria
│       └── L1.md            # L1 acceptance criteria
├── runs/                    # Run artifacts (L2+)
├── .github/workflows/
│   └── ci.yml               # GitHub Actions: lint + test on 3.10/3.11/3.12
├── AGENTS.md                # Agent contract (roles & rules)
├── Makefile                 # Dev commands
├── pyproject.toml           # Package config, ruff, pytest
├── bootstrap.sh             # Scaffold generation script
└── LICENSE                  # MIT
```

---

## Development

All common tasks are available via `make`:

| Command | Description |
|---|---|
| `make install` | Install package in editable mode with dev dependencies |
| `make test` | Run `pytest -q` |
| `make lint` | Check with `ruff check` and `ruff format --check` |
| `make fmt` | Auto-fix lint issues and format code |
| `make run` | Print CLI help |

**CI** runs on every push and pull request across Python 3.10, 3.11, and 3.12,
executing both lint and test steps.

---

## How the Ladder Works

Each level in the swarm ladder builds on the last and follows a strict workflow:

1. **Work order** -- A spec is written in `docs/work_orders/L<n>.md` with
   explicit acceptance criteria.
2. **Implementation** -- Code is added to `src/agent_lab/`, touching only what
   the level requires.
3. **Tests** -- Every acceptance criterion gets a corresponding test in
   `tests/`.
4. **CI gate** -- Nothing merges without a green check from GitHub Actions.

### L0: Deterministic CLI

Establishes the baseline: an installable Python package with a CLI entry point
(`agent-lab`), version printing, and a deterministic `hello` command. Proves
that the repo can ship changes with a passing CI pipeline.

### L1: Single Agent + One Tool Call

Introduces the `ToolResult` dataclass -- a structured JSON envelope that every
tool invocation returns:

| Field | Type | Description |
|---|---|---|
| `tool` | `str` | Tool name (e.g. `run_tests`) |
| `status` | `pass \| fail \| error` | Outcome |
| `command` | `str` | Exact command executed |
| `exit_code` | `int` | Process exit code |
| `stdout_tail` | `str` | Last 800 chars of stdout |
| `stderr_tail` | `str` | Last 800 chars of stderr |

The single tool (`run_tests`) executes `pytest -q` and wraps the result in this
structure. A `--dry-run` mode returns a sample result without running anything,
and `--selftest` provides a fast deterministic path for unit tests.

### L2 -- L5 (Planned)

- **L2** adds output validation and persists run artifacts to `runs/`.
- **L3** introduces multi-agent handoffs: Planner, Implementer, Tester.
- **L4** adds guardrails for risky actions and tracing of tool calls.
- **L5** brings full swarm orchestration with an eval suite measuring pass
  rate, loop count, tool error rate, and cost per run.

---

## Agent Contract

From [`AGENTS.md`](AGENTS.md) -- the rules that govern both human and AI
contributions to this repo:

| Role | Scope |
|---|---|
| **Planner** | Spec + acceptance criteria only |
| **Implementer** | Code only |
| **Tester** | Tests only |
| **Reviewer** | Risks + checklist |

**Core rule:** _If it can't be verified, it doesn't ship._

---

## Contributing

1. Pick an open level or issue.
2. Write a work order in `docs/work_orders/` with clear acceptance criteria.
3. Implement in a feature branch.
4. Ensure `make lint` and `make test` pass locally.
5. Open a pull request -- CI must be green before merge.

To install the optional agent dependencies (for levels that call OpenAI):

```bash
pip install -e ".[agents]"
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

---

## License

[MIT](LICENSE) -- Copyright (c) 2026 IT Pro Direct
