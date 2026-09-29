import subprocess
import sys
import os
import time
from typing import Dict, Any, Optional
from agent.models.execution_result import ExecutionResult

class SandboxExecutionEngine:
    """
    Phase 5 Module: Runs code in an isolated local subprocess sandbox,
    manages dependency installation, executes build/compile checks, and captures logs.
    """

    def __init__(self, timeout_seconds: int = 30):
        self.timeout_seconds = timeout_seconds

    def install_dependencies(self, project_dir: str) -> ExecutionResult:
        """
        Installs dependencies for the project based on detected files.
        """
        req_file = os.path.join(project_dir, "requirements.txt")
        package_json = os.path.join(project_dir, "package.json")

        if os.path.exists(req_file):
            cmd = f"{sys.executable} -m pip install -r requirements.txt"
            return self.run_command(cmd, cwd=project_dir)
        elif os.path.exists(package_json):
            cmd = "npm install"
            return self.run_command(cmd, cwd=project_dir)
        
        return ExecutionResult(
            command="install",
            exit_code=0,
            stdout="No dependency manifest found; skipped installation.",
            stderr=""
        )

    def verify_build(self, project_dir: str, primary_language: str = "python") -> ExecutionResult:
        """
        Performs build/compile verification on generated code.
        """
        if primary_language.lower() == "python":
            main_file = os.path.join(project_dir, "main.py")
            if os.path.exists(main_file):
                cmd = f"{sys.executable} -m py_compile main.py"
                return self.run_command(cmd, cwd=project_dir)
        elif primary_language.lower() == "java":
            return self.run_command("javac src/main/java/com/app/Application.java", cwd=project_dir)
        
        return ExecutionResult(command="verify_build", exit_code=0, stdout="Build verification skipped.", stderr="")

    def run_command(self, command: str, cwd: str, timeout: Optional[int] = None) -> ExecutionResult:
        """
        Executes a shell command inside the sandbox directory and captures outputs.
        """
        t0 = time.time()
        effective_timeout = timeout if timeout is not None else self.timeout_seconds
        try:
            res = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=effective_timeout
            )
            duration = time.time() - t0
            return ExecutionResult(
                command=command,
                exit_code=res.returncode,
                stdout=res.stdout,
                stderr=res.stderr,
                duration_seconds=duration
            )
        except subprocess.TimeoutExpired as e:
            duration = time.time() - t0
            return ExecutionResult(
                command=command,
                exit_code=124,
                stdout=e.stdout or "",
                stderr=f"Command timed out after {effective_timeout} seconds.",
                duration_seconds=duration
            )
        except Exception as e:
            duration = time.time() - t0
            return ExecutionResult(
                command=command,
                exit_code=1,
                stdout="",
                stderr=str(e),
                duration_seconds=duration
            )
