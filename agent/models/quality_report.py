from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class QualityReport:
    """
    Phase 8 Data Model: Static Code Quality, Security Vulnerabilities, and Refactoring Checks.
    """
    score: float = 100.0  # 0 to 100
    security_issues: List[Dict[str, Any]] = field(default_factory=list)
    code_smells: List[Dict[str, Any]] = field(default_factory=list)
    formatting_issues: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "score": self.score,
            "security_issues": self.security_issues,
            "code_smells": self.code_smells,
            "formatting_issues": self.formatting_issues,
            "recommendations": self.recommendations,
        }
