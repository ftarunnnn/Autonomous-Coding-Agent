import os
import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase9_documentation.doc_builder import DocumentationBuilder

def test_phase9_documentation_generation(tmp_path):
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()
    builder = DocumentationBuilder()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir=str(tmp_path))

    docs = builder.generate_documentation(spec, plan, str(tmp_path))

    assert "README.md" in docs
    assert "API_DOCS.md" in docs
    assert "ARCHITECTURE.md" in docs

    assert os.path.exists(tmp_path / "README.md")
    assert os.path.exists(tmp_path / "API_DOCS.md")
    assert os.path.exists(tmp_path / "ARCHITECTURE.md")
    assert "API Documentation" in (tmp_path / "API_DOCS.md").read_text()
