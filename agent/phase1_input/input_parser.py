import re
from typing import Dict, Any, List, Optional
from agent.models.task_spec import TaskSpec

class RequirementInputParser:
    """
    Phase 1 Module: Converts raw natural language prompt into a structured TaskSpec.
    """

    LANGUAGES = {
        "java": ["java", "spring", "springboot", "maven", "gradle"],
        "python": ["python", "fastapi", "flask", "django", "pytest"],
        "javascript": ["javascript", "node", "express", "js", "react"],
        "typescript": ["typescript", "ts", "nest", "next", "angular"],
        "go": ["go", "golang", "gin", "fiber"],
    }

    FRAMEWORKS = {
        "fastapi": ["fastapi"],
        "flask": ["flask"],
        "django": ["django"],
        "spring_boot": ["spring", "springboot", "spring boot"],
        "express": ["express", "expressjs"],
        "nest": ["nestjs", "nest"],
        "next": ["next.js", "nextjs"],
        "gin": ["gin"],
    }

    DATABASES = {
        "mysql": ["mysql", "mariadb"],
        "postgresql": ["postgres", "postgresql", "psql"],
        "sqlite": ["sqlite", "sqlite3"],
        "mongodb": ["mongo", "mongodb"],
        "redis": ["redis"],
    }

    def parse(self, raw_prompt: str) -> TaskSpec:
        """
        Parses a natural language requirement into a structured TaskSpec.
        """
        prompt_lower = raw_prompt.lower()
        
        # 1. Detect Language
        detected_language = "python"  # Default
        for lang, keywords in self.LANGUAGES.items():
            if any(kw in prompt_lower for kw in keywords):
                detected_language = lang
                break

        # 2. Detect Framework
        detected_framework = None
        for fw, keywords in self.FRAMEWORKS.items():
            if any(kw in prompt_lower for kw in keywords):
                detected_framework = fw
                break

        if not detected_framework:
            if detected_language == "python":
                detected_framework = "fastapi"
            elif detected_language == "java":
                detected_framework = "spring_boot"
            elif detected_language in ["javascript", "typescript"]:
                detected_framework = "express"
            elif detected_language == "go":
                detected_framework = "gin"

        # 3. Detect Database
        detected_db = None
        for db, keywords in self.DATABASES.items():
            if any(kw in prompt_lower for kw in keywords):
                detected_db = db
                break
        if not detected_db:
            detected_db = "sqlite"

        # 4. Infer Project Name
        project_name = self._infer_project_name(raw_prompt)

        # 5. Feature Extraction
        features = self._extract_features(raw_prompt)

        # 6. Infer Endpoints
        endpoints = self._infer_endpoints(raw_prompt, features)

        spec = TaskSpec(
            raw_prompt=raw_prompt,
            project_name=project_name,
            description=f"Automated project generated for: {raw_prompt}",
            primary_language=detected_language,
            framework=detected_framework,
            database=detected_db,
            requested_features=features,
            api_endpoints=endpoints,
            environment_variables={
                "DATABASE_URL": f"{detected_db}:///app.db" if detected_db == "sqlite" else f"{detected_db}://localhost:5432/app",
                "PORT": "8000",
                "ENV": "development"
            },
            is_complete=len(features) > 0
        )
        return spec

    def _infer_project_name(self, prompt: str) -> str:
        # Match pattern like "student management API" -> "student_management_api"
        clean = re.sub(r'[^a-zA-Z0-9\s]', '', prompt).strip()
        words = clean.split()
        if len(words) >= 2:
            return "_".join(words[:3]).lower()
        return "autonomous_app"

    def _extract_features(self, prompt: str) -> List[str]:
        features = []
        lower = prompt.lower()
        if "student" in lower:
            features.extend(["Student Enrollment", "Student CRUD", "Grade Tracking"])
        if "management" in lower or "api" in lower:
            features.append("RESTful API Endpoints")
        if "user" in lower or "auth" in lower or "login" in lower:
            features.extend(["User Authentication", "JWT Tokens"])
        if "blog" in lower or "post" in lower:
            features.extend(["Post Creation", "Comments", "Category Filtering"])
        if not features:
            features = ["Core CRUD Operations", "Health Check Endpoint"]
        return features

    def _infer_endpoints(self, prompt: str, features: List[str]) -> List[Dict[str, Any]]:
        endpoints = [
            {"method": "GET", "path": "/health", "description": "System health check"},
        ]
        lower = prompt.lower()
        resource = "items"
        if "student" in lower:
            resource = "students"
        elif "user" in lower:
            resource = "users"
        elif "blog" in lower or "post" in lower:
            resource = "posts"

        endpoints.extend([
            {"method": "GET", "path": f"/api/v1/{resource}", "description": f"List all {resource}"},
            {"method": "POST", "path": f"/api/v1/{resource}", "description": f"Create new {resource[:-1] if resource.endswith('s') else resource}"},
            {"method": "GET", "path": f"/api/v1/{resource}/{{id}}", "description": f"Get {resource[:-1] if resource.endswith('s') else resource} by ID"},
            {"method": "PUT", "path": f"/api/v1/{resource}/{{id}}", "description": f"Update {resource[:-1] if resource.endswith('s') else resource}"},
            {"method": "DELETE", "path": f"/api/v1/{resource}/{{id}}", "description": f"Delete {resource[:-1] if resource.endswith('s') else resource}"},
        ])
        return endpoints
