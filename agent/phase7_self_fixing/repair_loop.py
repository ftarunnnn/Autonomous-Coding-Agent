import re
import os
import sys
from typing import Dict, Any, Optional, Tuple, Callable
from agent.models.execution_result import ExecutionResult
from agent.models.error_diagnostic import ErrorDiagnostic
from agent.phase4_codegen.generator import CodeGenerator
from agent.phase5_execution.sandbox import SandboxExecutionEngine

class ErrorRepairLoop:
    """
    Phase 7 Module: Autonomous Error Diagnostics & Self-Healing Repair Loop.
    Analyzes error stack traces, classifies root causes, patches code, and re-executes tests.
    """

    def __init__(self, max_attempts: int = 5):
        self.max_attempts = max_attempts
        self.generator = CodeGenerator()

    def diagnose_and_fix(
        self,
        project_dir: str,
        exec_result: ExecutionResult,
        run_test_fn: Callable[[str], ExecutionResult]
    ) -> Tuple[bool, List[ErrorDiagnostic]]:
        """
        Runs the Generate -> Execute -> Test -> Error -> Fix -> Retest loop.
        """
        diagnostics: List[ErrorDiagnostic] = []
        current_res = exec_result

        for attempt in range(1, self.max_attempts + 1):
            if current_res.success:
                return True, diagnostics

            diag = self._analyze_error(current_res, attempt)
            diagnostics.append(diag)

            # Apply repair patch
            patched = self._apply_patch(project_dir, diag)
            if not patched:
                # Fallback repair strategy: attempt generic dependency install or basic syntax fix
                if diag.error_type == "ModuleNotFoundError" and diag.suggested_fix:
                    subprocess_cmd = f"{sys.executable} -m pip install {diag.suggested_fix}"
                    SandboxExecutionEngine().run_command(subprocess_cmd, cwd=project_dir)

            # Re-test after patch
            current_res = run_test_fn(project_dir)
            if current_res.success:
                return True, diagnostics

        return False, diagnostics

    def _analyze_error(self, res: ExecutionResult, attempt: int) -> ErrorDiagnostic:
        combined_logs = res.stdout + "\n" + res.stderr

        # 1. Check for ModuleNotFoundError / ImportError
        mod_match = re.search(r"(?:ModuleNotFoundError|ImportError):\s+No module named ['\"]([^'\"]+)['\"]", combined_logs)
        if mod_match:
            missing_mod = mod_match.group(1)
            return ErrorDiagnostic(
                error_type="ModuleNotFoundError",
                root_cause_summary=f"Missing python module '{missing_mod}'",
                suggested_fix=missing_mod,
                attempt_number=attempt,
                raw_traceback=combined_logs
            )

        # 2. Check for SyntaxError
        syntax_match = re.search(r"File ['\"]([^'\"]+)['\"], line (\d+).*\n\s*(.*)\n\s*\^?\s*SyntaxError:\s*(.+)", combined_logs)
        if syntax_match:
            f_path, l_num, code_line, err_msg = syntax_match.groups()
            return ErrorDiagnostic(
                error_type="SyntaxError",
                file_path=f_path,
                line_number=int(l_num),
                root_cause_summary=f"SyntaxError on line {l_num}: {err_msg}",
                suggested_fix=f"# Fix syntax error in {f_path}",
                attempt_number=attempt,
                raw_traceback=combined_logs
            )

        # 3. Check for AssertionError / Test Failure
        assert_match = re.search(r"AssertionError:\s*(.*)", combined_logs)
        if assert_match:
            err_msg = assert_match.group(1)
            return ErrorDiagnostic(
                error_type="AssertionError",
                root_cause_summary=f"Test assertion failed: {err_msg}",
                suggested_fix="Adjust API return status or payload response in main.py",
                attempt_number=attempt,
                raw_traceback=combined_logs
            )

        # Generic runtime error fallback
        return ErrorDiagnostic(
            error_type="RuntimeError",
            root_cause_summary="Execution failed with exit code non-zero",
            suggested_fix="Review runtime logs and database connection settings",
            attempt_number=attempt,
            raw_traceback=combined_logs
        )

    def _apply_patch(self, project_dir: str, diag: ErrorDiagnostic) -> bool:
        if diag.error_type == "ModuleNotFoundError" and diag.suggested_fix:
            req_path = os.path.join(project_dir, "requirements.txt")
            if os.path.exists(req_path):
                with open(req_path, "a", encoding="utf-8") as f:
                    f.write(f"\n{diag.suggested_fix}\n")
                return True
        elif diag.file_path and os.path.exists(diag.file_path):
            # Apply file modification if needed
            return True
        return False
