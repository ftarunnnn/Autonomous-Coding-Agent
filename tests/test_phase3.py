import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer
from agent.phase3_planning.planner import ProjectPlanner

def test_phase3_planning():
    parser = RequirementInputParser()
    analyzer = RequirementAnalyzer()
    planner = ProjectPlanner()

    spec = parser.parse("Build a student management API using Python + SQLite")
    spec, _ = analyzer.analyze(spec)
    plan = planner.plan(spec, target_dir="generated_student_app")

    assert plan.project_name == spec.project_name
    assert len(plan.folder_structure) > 0
    assert len(plan.file_manifest) >= 5
    assert len(plan.task_dag) == len(plan.file_manifest)
    assert len(plan.db_schema.get("tables", [])) >= 1
