import os
import sys
import re
from typing import Dict, Any, List
from agent.models.task_spec import TaskSpec
from agent.models.execution_result import ExecutionResult
from agent.phase5_execution.sandbox import SandboxExecutionEngine

class AutomatedTester:
    """
    Phase 6 Module: Generates automated unit and integration tests for the project,
    executes them inside the sandbox, and parses pass/fail metrics & traces.
    """

    def generate_tests(self, spec: TaskSpec, project_dir: str) -> str:
        """
        Generates pytest test suite file inside project_dir/tests/test_api.py
        """
        tests_dir = os.path.join(project_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)

        entities = spec.metadata.get("entities", [])
        primary_entity = entities[0]["name"] if entities else "Item"
        entity_plural = primary_entity.lower() + "s"

        test_content = f"""import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_and_get_{primary_entity.lower()}():
    payload = {{"name": "Test {primary_entity}", "detail": "Automated test item", "status": "active"}}
    create_res = client.post("/api/v1/{entity_plural}", json=payload)
    assert create_res.status_code == 200
    data = create_res.json()
    assert "id" in data
    assert data["name"] == payload["name"]

    item_id = data["id"]
    get_res = client.get(f"/api/v1/{entity_plural}/{{item_id}}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == payload["name"]

def test_list_{entity_plural}():
    response = client.get("/api/v1/{entity_plural}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_{primary_entity.lower()}():
    # Create item to delete
    create_res = client.post("/api/v1/{entity_plural}", json={{"name": "To Delete", "detail": "Temp"}})
    item_id = create_res.json()["id"]

    del_res = client.delete(f"/api/v1/{entity_plural}/{{item_id}}")
    assert del_res.status_code == 200

    # Confirm deleted
    get_res = client.get(f"/api/v1/{entity_plural}/{{item_id}}")
    assert get_res.status_code == 404
"""
        test_path = os.path.join(tests_dir, "test_api.py")
        with open(test_path, "w", encoding="utf-8") as f:
            f.write(test_content)

        return test_path

    def run_tests(self, project_dir: str, sandbox: SandboxExecutionEngine) -> ExecutionResult:
        """
        Executes pytest test suite inside the project sandbox and parses test results.
        """
        cmd = f"{sys.executable} -m pytest tests/ -v"
        res = sandbox.run_command(cmd, cwd=project_dir)
        
        passed, failed, details = self._parse_pytest_output(res.stdout, res.stderr)
        res.passed_tests = passed
        res.failed_tests = failed
        res.test_details = details
        return res

    def _parse_pytest_output(self, stdout: str, stderr: str) -> tuple[int, int, List[Dict[str, Any]]]:
        combined = stdout + "\n" + stderr
        passed_match = re.search(r'(\d+)\s+passed', combined)
        failed_match = re.search(r'(\d+)\s+failed', combined)

        passed = int(passed_match.group(1)) if passed_match else 0
        failed = int(failed_match.group(1)) if failed_match else 0

        details = []
        if failed > 0:
            failures = re.findall(r'FAILED\s+([^\s]+)\s+-\s+(.+)', combined)
            for f_test, f_reason in failures:
                details.append({"test": f_test, "error": f_reason})

        return passed, failed, details
