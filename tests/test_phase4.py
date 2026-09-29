import os
import shutil
import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner
from agent.phase4_codegen.generator import CodeGenerator

def test_phase4_code_generation_and_patching(tmp_path):
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()
    generator = CodeGenerator()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir=str(tmp_path))

    generated_files = generator.generate_project(spec, plan, output_dir=str(tmp_path))

    assert "main.py" in generated_files
    assert os.path.exists(tmp_path / "main.py")
    assert "FastAPI" in (tmp_path / "main.py").read_text()

    # Test File Patching
    patched = generator.patch_file(
        str(tmp_path / "main.py"),
        old_snippet='version="1.0.0"',
        new_snippet='version="2.0.0"'
    )
    assert patched is True
    assert 'version="2.0.0"' in (tmp_path / "main.py").read_text()
