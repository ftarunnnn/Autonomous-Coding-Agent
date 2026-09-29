from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ErrorDiagnostic:
    """
    Phase 7 Data Model: Stack trace analysis, root cause diagnosis, and repair actions.
    """
    error_type: str  # SyntaxError, ImportError, RuntimeError, AssertionError, TimeoutError, etc.
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    raw_traceback: str = ""
    root_cause_summary: str = ""
    suggested_fix: str = ""
    patched_files: List[str] = field(default_factory=list)
    attempt_number: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.error_type,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "raw_traceback": self.raw_traceback,
            "root_cause_summary": self.root_cause_summary,
            "suggested_fix": self.suggested_fix,
            "patched_files": self.patched_files,
            "attempt_number": self.attempt_number,
        }
