import os
import re
from typing import Dict, Any, List
from agent.models.quality_report import QualityReport

class QualityAndSecurityChecker:
    """
    Phase 8 Module: Audits code quality, checks for hardcoded credentials,
    SQL injection risks, input validation, and code smells.
    """

    SECRET_PATTERNS = [
        (r"(?i)(api_key|secret_key|password|token)\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "Hardcoded API Key / Secret"),
        (r"(?i)bearer\s+[A-Za-z0-9_\-\.]{20,}", "Hardcoded Bearer Token"),
    ]

    SQL_INJECTION_PATTERNS = [
        (r"(?i)SELECT\s+.*\s+FROM\s+.*\+.*", "Potential SQL Injection via string concatenation"),
        (r"(?i)execute\s*\(\s*f['\"].*SELECT.*\{.*\}", "Potential SQL Injection via f-string formatting"),
    ]

    def audit_project(self, project_dir: str) -> QualityReport:
        """
        Audits all source files in project_dir for code smells, security vulnerabilities, and quality.
        """
        security_issues = []
        code_smells = []
        formatting_issues = []
        recommendations = []
        total_files = 0

        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith((".py", ".js", ".java")):
                    total_files += 1
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, project_dir)
                    
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # 1. Hardcoded Secret Check
                    for pattern, desc in self.SECRET_PATTERNS:
                        if re.search(pattern, content):
                            security_issues.append({"file": rel_path, "issue": desc, "severity": "HIGH"})

                    # 2. SQL Injection Check
                    for pattern, desc in self.SQL_INJECTION_PATTERNS:
                        if re.search(pattern, content):
                            security_issues.append({"file": rel_path, "issue": desc, "severity": "CRITICAL"})

                    # 3. Input Validation Check
                    if "BaseModel" not in content and "pydantic" not in content and "routes" in rel_path:
                        code_smells.append({"file": rel_path, "issue": "Missing formal request body validation schema"})

                    # 4. Empty Exception Handler Check
                    if re.search(r"except\s*:\s*pass", content):
                        code_smells.append({"file": rel_path, "issue": "Bare except clause swallowing errors silently"})

        # Calculate Score
        deductions = (len(security_issues) * 20) + (len(code_smells) * 10)
        score = max(0.0, 100.0 - deductions)

        if security_issues:
            recommendations.append("Move hardcoded credentials and database connection strings to environment variables.")
        if code_smells:
            recommendations.append("Enforce explicit Pydantic / DTO schemas for API request validation.")
        if not recommendations:
            recommendations.append("Code passes baseline security and quality standards.")

        return QualityReport(
            score=score,
            security_issues=security_issues,
            code_smells=code_smells,
            formatting_issues=formatting_issues,
            recommendations=recommendations
        )
