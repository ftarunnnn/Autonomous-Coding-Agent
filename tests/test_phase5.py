import os
import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase4_codegen.generator import CodeGenerator
from agent.phase5_execution.sandbox import SandboxExecutionEngine

def test_phase5_execution_and_compilation(tmp_path):
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()
    generator = CodeGenerator()
    sandbox = SandboxExecutionEngine()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir=str(tmp_path))
    generator.generate_project(spec, plan, output_dir=str(tmp_path))

    # Verify build compilation
    build_result = sandbox.verify_build(str(tmp_path), primary_language="python")
    assert build_result.exit_code == 0

    # Run echo command inside sandbox
    cmd_result = sandbox.run_command("python -c \"print('Sandbox active')\"", cwd=str(tmp_path))
    assert cmd_result.exit_code == 0
    assert "Sandbox active" in cmd_result.stdout
