import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase4_codegen.generator import CodeGenerator
from agent.phase8_quality.quality_checker import QualityAndSecurityChecker

def test_phase8_security_and_quality_audit(tmp_path):
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()
    generator = CodeGenerator()
    checker = QualityAndSecurityChecker()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir=str(tmp_path))
    generator.generate_project(spec, plan, output_dir=str(tmp_path))

    report = checker.audit_project(str(tmp_path))

    assert report.score >= 80.0
    assert isinstance(report.security_issues, list)
    assert isinstance(report.recommendations, list)

def test_phase8_detect_vulnerability(tmp_path):
    checker = QualityAndSecurityChecker()

    bad_file = tmp_path / "bad.py"
    bad_file.write_text("api_key = '1234567890123456789'\ncursor.execute(f'SELECT * FROM users WHERE name = {user}')\n")

    report = checker.audit_project(str(tmp_path))

    assert len(report.security_issues) >= 1
    assert report.score < 100.0
