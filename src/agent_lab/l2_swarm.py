from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .artifacts import run_dir, workspace_dir, write_json, write_text


@dataclass(frozen=True)
class PlanStep:
    id: str
    role: str
    action: str
    acceptance: list[str]


@dataclass(frozen=True)
class Plan:
    level: str
    run_id: str
    task: str
    constraints: dict[str, Any]
    steps: list[PlanStep]
    acceptance: list[str]


def coordinator_make_plan(*, task: str, run_id: str) -> Plan:
    constraints = {
        "allowed_write_root": str(workspace_dir(run_id)),
        "no_repo_writes": True,
        "max_steps": 3,
    }
    steps = [
        PlanStep(
            id="step_1",
            role="implementer",
            action="Create workspace marker file hello.txt with deterministic content.",
            acceptance=[
                "workspace/hello.txt exists",
                "workspace/hello.txt content matches expected",
            ],
        )
    ]
    return Plan(
        level="L2",
        run_id=run_id,
        task=task,
        constraints=constraints,
        steps=steps,
        acceptance=["plan artifacts written", "result.json written"],
    )


def plan_to_markdown(plan: Plan) -> str:
    lines: list[str] = []
    lines.append(f"# {plan.level} Plan")
    lines.append("")
    lines.append(f"- run_id: `{plan.run_id}`")
    lines.append(f"- task: `{plan.task}`")
    lines.append("")
    lines.append("## Constraints")
    for k in sorted(plan.constraints.keys()):
        lines.append(f"- {k}: {plan.constraints[k]}")
    lines.append("")
    lines.append("## Steps")
    for step in plan.steps:
        lines.append(f"### {step.id} ({step.role})")
        lines.append(f"- action: {step.action}")
        lines.append("- acceptance:")
        for a in step.acceptance:
            lines.append(f"  - {a}")
        lines.append("")
    lines.append("## Final Acceptance")
    for a in plan.acceptance:
        lines.append(f"- {a}")
    lines.append("")
    return "\n".join(lines)


def implementer_execute_step(*, plan: Plan, step: PlanStep) -> dict[str, Any]:
    ws = Path(plan.constraints["allowed_write_root"])
    ws.mkdir(parents=True, exist_ok=True)

    target = ws / "hello.txt"
    expected = "hello from L2 implementer\n"
    target.write_text(expected, encoding="utf-8")

    checks = [
        {"name": "hello_exists", "ok": target.exists()},
        {"name": "hello_content", "ok": target.read_text(encoding="utf-8") == expected},
    ]

    return {"step_id": step.id, "ok": all(c["ok"] for c in checks), "checks": checks}


def run_l2(*, task: str, run_id: str) -> dict[str, Any]:
    rd = run_dir(run_id)
    ws = workspace_dir(run_id)
    rd.mkdir(parents=True, exist_ok=True)
    ws.mkdir(parents=True, exist_ok=True)

    plan = coordinator_make_plan(task=task, run_id=run_id)

    write_json(rd / "plan.json", plan)
    write_text(rd / "plan.md", plan_to_markdown(plan))

    step = plan.steps[0]
    step_result = implementer_execute_step(plan=plan, step=step)

    write_text(rd / "diff.patch", "")

    result = {
        "level": plan.level,
        "run_id": plan.run_id,
        "task": plan.task,
        "ok": bool(step_result["ok"]),
        "step_result": step_result,
    }
    write_json(rd / "result.json", result)
    return result
