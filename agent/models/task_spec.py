from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import uuid

@dataclass
class TaskSpec:
    """
    Phase 1 Data Model: Structured Representation of User Requirement.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    raw_prompt: str = ""
    project_name: str = ""
    description: str = ""
    primary_language: str = "python"  # python, java, javascript, typescript, go, etc.
    framework: Optional[str] = None    # fastapi, flask, spring, express, react, etc.
    database: Optional[str] = None     # sqlite, mysql, postgresql, mongodb, etc.
    requested_features: List[str] = field(default_factory=list)
    api_endpoints: List[Dict[str, Any]] = field(default_factory=list)
    environment_variables: Dict[str, str] = field(default_factory=dict)
    clarifications_needed: List[str] = field(default_factory=list)
    is_complete: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "raw_prompt": self.raw_prompt,
            "project_name": self.project_name,
            "description": self.description,
            "primary_language": self.primary_language,
            "framework": self.framework,
            "database": self.database,
            "requested_features": self.requested_features,
            "api_endpoints": self.api_endpoints,
            "environment_variables": self.environment_variables,
            "clarifications_needed": self.clarifications_needed,
            "is_complete": self.is_complete,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskSpec":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            raw_prompt=data.get("raw_prompt", ""),
            project_name=data.get("project_name", ""),
            description=data.get("description", ""),
            primary_language=data.get("primary_language", "python"),
            framework=data.get("framework"),
            database=data.get("database"),
            requested_features=data.get("requested_features", []),
            api_endpoints=data.get("api_endpoints", []),
            environment_variables=data.get("environment_variables", {}),
            clarifications_needed=data.get("clarifications_needed", []),
            is_complete=data.get("is_complete", False),
            metadata=data.get("metadata", {}),
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
