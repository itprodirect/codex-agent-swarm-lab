from __future__ import annotations

import json
from pathlib import Path

from agent_lab.l2_swarm import run_l2


def test_l2_selftest_creates_artifacts(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SWARM_LAB_RUNS_DIR", str(tmp_path / "runs"))

    result = run_l2(task="selftest", run_id="test")
    assert result["ok"] is True

    rd = tmp_path / "runs" / "test"
    assert (rd / "plan.json").exists()
    assert (rd / "plan.md").exists()
    assert (rd / "diff.patch").exists()
    assert (rd / "result.json").exists()

    plan = json.loads((rd / "plan.json").read_text(encoding="utf-8"))
    assert plan["level"] == "L2"
    assert plan["run_id"] == "test"
    assert plan["steps"][0]["role"] == "implementer"


def test_l2_is_deterministic(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("SWARM_LAB_RUNS_DIR", str(tmp_path / "runs"))

    r1 = run_l2(task="selftest", run_id="test")
    r2 = run_l2(task="selftest", run_id="test")

    assert r1 == r2
    rd = tmp_path / "runs" / "test"
    assert (rd / "plan.json").read_text(encoding="utf-8") == (rd / "plan.json").read_text(
        encoding="utf-8"
    )
