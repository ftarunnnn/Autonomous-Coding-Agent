import pytest
from agent.models.execution_result import ExecutionResult
from agent.phase7_self_fixing.repair_loop import ErrorRepairLoop

def test_phase7_error_diagnosis():
    repair_loop = ErrorRepairLoop()

    # Simulate ModuleNotFoundError execution result
    failed_res = ExecutionResult(
        command="pytest",
        exit_code=1,
        stdout="",
        stderr="ModuleNotFoundError: No module named 'httpx'"
    )

    diag = repair_loop._analyze_error(failed_res, attempt=1)
    assert diag.error_type == "ModuleNotFoundError"
    assert diag.suggested_fix == "httpx"

def test_phase7_repair_loop_recovery(tmp_path):
    repair_loop = ErrorRepairLoop()

    # Create dummy project dir with requirements.txt
    req_file = tmp_path / "requirements.txt"
    req_file.write_text("fastapi\n")

    failed_res = ExecutionResult(
        command="pytest",
        exit_code=1,
        stdout="",
        stderr="ModuleNotFoundError: No module named 'pytest_mock'"
    )

    # Mock test function that succeeds on retry 2
    calls = []
    def mock_run_test(p_dir):
        calls.append(p_dir)
        if len(calls) == 1:
            return ExecutionResult(command="pytest", exit_code=0, stdout="1 passed", stderr="")
        return ExecutionResult(command="pytest", exit_code=1, stdout="", stderr="failed")

    success, diagnostics = repair_loop.diagnose_and_fix(str(tmp_path), failed_res, mock_run_test)
    assert success is True
    assert len(diagnostics) == 1
    assert "pytest_mock" in req_file.read_text()
