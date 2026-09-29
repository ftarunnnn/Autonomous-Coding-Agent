import pytest
from agent.phase1_input.input_parser import RequirementInputParser

def test_phase1_requirement_parsing():
    parser = RequirementInputParser()
    prompt = "Build a student management API using Java + MySQL"
    spec = parser.parse(prompt)

    assert spec.raw_prompt == prompt
    assert spec.primary_language == "java"
    assert spec.framework == "spring_boot"
    assert spec.database == "mysql"
    assert "Student Enrollment" in spec.requested_features or "Student CRUD" in spec.requested_features
    assert len(spec.api_endpoints) >= 5

def test_phase1_python_fastapi_parsing():
    parser = RequirementInputParser()
    prompt = "Create a blog platform in Python FastAPI with PostgreSQL"
    spec = parser.parse(prompt)

    assert spec.primary_language == "python"
    assert spec.framework == "fastapi"
    assert spec.database == "postgresql"
    assert len(spec.api_endpoints) >= 5
