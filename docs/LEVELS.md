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
