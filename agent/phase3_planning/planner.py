from typing import Dict, Any, List
from agent.models.task_spec import TaskSpec
from agent.models.architecture_plan import ArchitecturePlan

class ProjectPlanner:
    """
    Phase 3 Module: Architectures directory structure, file manifest, DB DDL schemas,
    and Task Dependency DAG based on TaskSpec.
    """

    def plan(self, spec: TaskSpec, target_dir: str = "generated_app") -> ArchitecturePlan:
        """
        Creates a comprehensive ArchitecturePlan for the project.
        """
        lang = spec.primary_language.lower()
        fw = (spec.framework or "").lower()

        folder_structure, manifest = self._build_structure(lang, fw)
        db_schema = self._build_db_schema(spec)
        task_dag = self._build_task_dag(spec, manifest)
        dependencies = self._build_dependencies(lang, fw, spec.database)

        return ArchitecturePlan(
            project_name=spec.project_name,
            root_directory=target_dir,
            folder_structure=folder_structure,
            file_manifest=manifest,
            modules=[
                {"name": "Core/Config", "description": "Configuration & Database Connection Setup"},
                {"name": "Models", "description": "ORM Data Models & Schemas"},
                {"name": "Controllers/Routes", "description": "REST API Handlers & Routing"},
                {"name": "Services", "description": "Business logic & data access"},
                {"name": "Tests", "description": "Automated Unit & Integration Test Suites"}
            ],
            db_schema=db_schema,
            task_dag=task_dag,
            dependencies=dependencies
        )

    def _build_structure(self, lang: str, fw: str) -> tuple[List[str], List[Dict[str, str]]]:
        if lang == "python":
            folders = ["app", "app/models", "app/routes", "app/config", "app/services", "tests"]
            manifest = [
                {"path": "app/__init__.py", "description": "App initialization"},
                {"path": "app/config/settings.py", "description": "Environment variables & configuration"},
                {"path": "app/config/database.py", "description": "Database connection & session setup"},
                {"path": "app/models/schemas.py", "description": "Pydantic / Dataclass schemas"},
                {"path": "app/models/database.py", "description": "Database ORM models"},
                {"path": "app/routes/api.py", "description": "REST API route endpoints"},
                {"path": "main.py", "description": "Application entry point server"},
                {"path": "requirements.txt", "description": "Project Python dependencies"},
                {"path": "tests/test_api.py", "description": "API Integration Tests"}
            ]
        elif lang == "java":
            folders = [
                "src/main/java/com/app",
                "src/main/java/com/app/controller",
                "src/main/java/com/app/model",
                "src/main/java/com/app/repository",
                "src/main/java/com/app/service",
                "src/main/resources",
                "src/test/java/com/app"
            ]
            manifest = [
                {"path": "src/main/java/com/app/Application.java", "description": "Spring Boot Main Entrypoint"},
                {"path": "src/main/java/com/app/model/EntityModel.java", "description": "JPA Entity Model"},
                {"path": "src/main/java/com/app/repository/EntityRepository.java", "description": "Spring Data JPA Repository"},
                {"path": "src/main/java/com/app/controller/ApiController.java", "description": "Spring REST Controller"},
                {"path": "src/main/resources/application.properties", "description": "Spring Boot Configuration"},
                {"path": "pom.xml", "description": "Maven dependencies build file"},
                {"path": "src/test/java/com/app/ApplicationTests.java", "description": "JUnit Test Suite"}
            ]
        else: # Node / Express / JS
            folders = ["src", "src/controllers", "src/models", "src/routes", "src/config", "tests"]
            manifest = [
                {"path": "src/server.js", "description": "Express server entrypoint"},
                {"path": "src/config/db.js", "description": "Database driver setup"},
                {"path": "src/models/itemModel.js", "description": "Data models"},
                {"path": "src/routes/apiRoutes.js", "description": "Express Router handlers"},
                {"path": "package.json", "description": "NPM manifest & scripts"},
                {"path": "tests/api.test.js", "description": "Jest test suite"}
            ]
        return folders, manifest

    def _build_db_schema(self, spec: TaskSpec) -> Dict[str, Any]:
        entities = spec.metadata.get("entities", [])
        tables = []
        for entity in entities:
            name = entity["name"].lower() + "s"
            cols = []
            for f in entity.get("fields", []):
                col_type = "INTEGER" if f["type"] == "int" else ("VARCHAR(255)" if f["type"] == "string" else "TEXT")
                pk = " PRIMARY KEY AUTOINCREMENT" if f.get("primary_key") else ""
                cols.append(f"{f['name']} {col_type}{pk}")
            ddl = f"CREATE TABLE IF NOT EXISTS {name} (\n  " + ",\n  ".join(cols) + "\n);"
            tables.append({"table_name": name, "ddl": ddl})
        return {"tables": tables}

    def _build_task_dag(self, spec: TaskSpec, manifest: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        tasks = []
        for idx, item in enumerate(manifest, 1):
            tasks.append({
                "task_id": f"TASK-{idx:02d}",
                "name": f"Create {item['path']}",
                "file_path": item["path"],
                "description": item["description"],
                "dependencies": [f"TASK-{idx-1:02d}"] if idx > 1 else []
            })
        return tasks

    def _build_dependencies(self, lang: str, fw: str, db: Optional[str]) -> List[str]:
        if lang == "python":
            deps = ["fastapi", "uvicorn", "pydantic", "pytest", "requests"]
            if db == "sqlite":
                deps.append("sqlite3")
            elif db == "mysql":
                deps.append("pymysql")
            elif db == "postgresql":
                deps.append("psycopg2-binary")
            return deps
        elif lang == "java":
            return ["spring-boot-starter-web", "spring-boot-starter-data-jpa", "mysql-connector-j", "junit-jupiter"]
        else:
            return ["express", "dotenv", "cors", "jest", "supertest"]
