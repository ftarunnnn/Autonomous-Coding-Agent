import os
import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase4_codegen.generator import CodeGenerator
from agent.phase5_execution.sandbox import SandboxExecutionEngine
from agent.phase6_testing.tester import AutomatedTester

def test_phase6_test_generation_and_execution(tmp_path):
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()
    generator = CodeGenerator()
    sandbox = SandboxExecutionEngine()
    tester = AutomatedTester()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir=str(tmp_path))
    generator.generate_project(spec, plan, output_dir=str(tmp_path))

    # Install httpx / test dependencies if needed by TestClient
    sandbox.run_command("python -m pip install httpx", cwd=str(tmp_path))

    test_path = tester.generate_tests(spec, str(tmp_path))
    assert os.path.exists(test_path)

    test_res = tester.run_tests(str(tmp_path), sandbox)
    assert test_res.passed_tests >= 3
    assert test_res.failed_tests == 0
