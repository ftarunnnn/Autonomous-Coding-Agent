from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExecutionResult:
    """
    Phase 5 & 6 Data Model: Subprocess Sandbox Execution & Test Results.
    """
    command: str
    exit_code: int
    stdout: str
    stderr: str
    duration_seconds: float = 0.0
    passed_tests: int = 0
    failed_tests: int = 0
    test_details: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return self.exit_code == 0 and self.failed_tests == 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command": self.command,
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": self.duration_seconds,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success": self.success,
            "test_details": self.test_details,
        }
