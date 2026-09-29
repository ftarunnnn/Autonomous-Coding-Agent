from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ArchitecturePlan:
    """
    Phase 3 Data Model: Project Architecture, Folder Structure & Task DAG.
    """
    project_name: str
    root_directory: str
    folder_structure: List[str] = field(default_factory=list)
    file_manifest: List[Dict[str, str]] = field(default_factory=list)  # {"path": relative_path, "description": summary}
    modules: List[Dict[str, Any]] = field(default_factory=list)
    db_schema: Dict[str, Any] = field(default_factory=dict)
    task_dag: List[Dict[str, Any]] = field(default_factory=list)  # list of sequential/parallel tasks
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_name": self.project_name,
            "root_directory": self.root_directory,
            "folder_structure": self.folder_structure,
            "file_manifest": self.file_manifest,
            "modules": self.modules,
            "db_schema": self.db_schema,
            "task_dag": self.task_dag,
            "dependencies": self.dependencies,
        }
