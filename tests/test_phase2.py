import pytest
from agent.phase1_input.input_parser import RequirementInputParser
from agent.phase2_analysis.analyzer import RequirementAnalyzer

def test_phase2_analysis_and_entity_inference():
    parser = RequirementInputParser()
    spec = parser.parse("Build a student management API using Java + MySQL")
    
    analyzer = RequirementAnalyzer()
    analyzed_spec, clarifications = analyzer.analyze(spec)

    assert "tech_stack" in analyzed_spec.metadata
    assert analyzed_spec.metadata["tech_stack"]["language"] == "java"
    assert "entities" in analyzed_spec.metadata
    entity_names = [e["name"] for e in analyzed_spec.metadata["entities"]]
    assert "Student" in entity_names
