import os
import pytest
from agent.orchestrator import AutonomousAgentOrchestrator

def test_full_10_phase_autonomous_loop(tmp_path):
    orchestrator = AutonomousAgentOrchestrator(workspace_root=str(tmp_path))
    prompt = "Build a student management API using Python + SQLite"

    target_dir = str(tmp_path / "student_app")
    results = orchestrator.run_pipeline(prompt, target_dir=target_dir)

    assert results["status"] == "success"
    assert len(results["phase_logs"]) == 10
    assert results["quality_score"] >= 70.0
    assert os.path.exists(os.path.join(target_dir, "main.py"))
    assert os.path.exists(os.path.join(target_dir, "README.md"))
    assert os.path.exists(os.path.join(target_dir, "Dockerfile"))
