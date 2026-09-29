from typing import Dict, Any, List, Tuple
from agent.models.task_spec import TaskSpec

class RequirementAnalyzer:
    """
    Phase 2 Module: Analyzes TaskSpec, identifies features, tech stack, data models,
    and detects missing requirements to prompt for clarification.
    """

    def analyze(self, spec: TaskSpec) -> Tuple[TaskSpec, List[str]]:
        """
        Analyzes the requirement, enriches TaskSpec with inferred entities/schemas,
        and returns list of clarification questions if any ambiguity exists.
        """
        clarifications = []
        metadata = dict(spec.metadata)

        # 1. Tech Stack Validation & Enrichment
        tech_stack_info = {
            "language": spec.primary_language,
            "framework": spec.framework,
            "database": spec.database,
            "package_manager": "pip" if spec.primary_language == "python" else ("maven" if spec.primary_language == "java" else "npm"),
            "test_runner": "pytest" if spec.primary_language == "python" else ("junit" if spec.primary_language == "java" else "jest")
        }
        metadata["tech_stack"] = tech_stack_info

        # 2. Entity Schema Inference
        entities = self._infer_entities(spec)
        metadata["entities"] = entities

        # 3. Missing Requirement & Clarification Detection
        if not spec.database:
            clarifications.append("Which database system do you prefer? (e.g., SQLite, PostgreSQL, MySQL)")
        
        if "User Authentication" in spec.requested_features and "auth_strategy" not in metadata:
            clarifications.append("Which authentication mechanism should be implemented? (e.g., JWT, OAuth2, Session)")
            metadata["auth_strategy"] = "JWT"  # Default assumption

        if not spec.requested_features:
            clarifications.append("Could you list the specific business features or resources needed?")

        spec.clarifications_needed = clarifications
        spec.metadata = metadata
        return spec, clarifications

    def _infer_entities(self, spec: TaskSpec) -> List[Dict[str, Any]]:
        prompt = spec.raw_prompt.lower()
        entities = []

        if "student" in prompt:
            entities.append({
                "name": "Student",
                "fields": [
                    {"name": "id", "type": "int", "primary_key": True, "auto_increment": True},
                    {"name": "name", "type": "string", "required": True},
                    {"name": "email", "type": "string", "required": True, "unique": True},
                    {"name": "course", "type": "string", "required": False},
                    {"name": "gpa", "type": "float", "required": False},
                    {"name": "created_at", "type": "datetime", "auto_now_add": True},
                ]
            })
            entities.append({
                "name": "Course",
                "fields": [
                    {"name": "id", "type": "int", "primary_key": True, "auto_increment": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "code", "type": "string", "required": True, "unique": True},
                    {"name": "credits", "type": "int", "required": True},
                ]
            })
        elif "blog" in prompt or "post" in prompt:
            entities.append({
                "name": "Post",
                "fields": [
                    {"name": "id", "type": "int", "primary_key": True, "auto_increment": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "content", "type": "text", "required": True},
                    {"name": "author", "type": "string", "required": True},
                    {"name": "created_at", "type": "datetime", "auto_now_add": True},
                ]
            })
        else:
            # Generic resource entity
            entities.append({
                "name": "Item",
                "fields": [
                    {"name": "id", "type": "int", "primary_key": True, "auto_increment": True},
                    {"name": "title", "type": "string", "required": True},
                    {"name": "description", "type": "string", "required": False},
                    {"name": "status", "type": "string", "default": "active"},
                ]
            })

        return entities
