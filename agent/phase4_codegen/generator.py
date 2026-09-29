import os
from typing import Dict, Any, List, Optional
from agent.models.task_spec import TaskSpec
from agent.models.architecture_plan import ArchitecturePlan

class CodeGenerator:
    """
    Phase 4 Module: Generates full working source code, configuration files,
    database models, and API endpoints, and supports patching existing files.
    """

    def generate_project(self, spec: TaskSpec, plan: ArchitecturePlan, output_dir: str) -> Dict[str, str]:
        """
        Generates all project files on disk and returns a dict mapping file paths to content.
        """
        generated_files = {}

        # 1. Ensure directory structure exists
        for folder in plan.folder_structure:
            full_folder = os.path.join(output_dir, folder)
            os.makedirs(full_folder, exist_ok=True)

        # 2. Generate Files based on language & framework
        lang = spec.primary_language.lower()
        if lang == "python":
            generated_files = self._generate_python_app(spec, plan, output_dir)
        elif lang == "java":
            generated_files = self._generate_java_app(spec, plan, output_dir)
        else:
            generated_files = self._generate_node_app(spec, plan, output_dir)

        # Write files to disk
        for rel_path, content in generated_files.items():
            full_path = os.path.join(output_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return generated_files

    def patch_file(self, file_path: str, old_snippet: str, new_snippet: str) -> bool:
        """
        Modifies an existing file by replacing old_snippet with new_snippet.
        """
        if not os.path.exists(file_path):
            return False
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if old_snippet in content:
            updated = content.replace(old_snippet, new_snippet)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated)
            return True
        return False

    def _generate_python_app(self, spec: TaskSpec, plan: ArchitecturePlan, output_dir: str) -> Dict[str, str]:
        files = {}
        entities = spec.metadata.get("entities", [])
        primary_entity = entities[0]["name"] if entities else "Item"
        entity_lower = primary_entity.lower()
        entity_plural = entity_lower + "s"

        # main.py
        files["main.py"] = f"""from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI(title="{spec.project_name.title()} API", version="1.0.0")

# Database setup
DB_NAME = "app.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS {entity_plural} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            detail TEXT,
            status TEXT DEFAULT 'active'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class {primary_entity}Create(BaseModel):
    name: str
    detail: Optional[str] = None
    status: Optional[str] = "active"

class {primary_entity}Response({primary_entity}Create):
    id: int

@app.get("/health")
def health_check():
    return {{"status": "healthy", "service": "{spec.project_name}"}}

@app.get("/api/v1/{entity_plural}", response_model=List[{primary_entity}Response])
def get_all_{entity_plural}():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, detail, status FROM {entity_plural}")
    rows = cursor.fetchall()
    conn.close()
    return [{{"id": r[0], "name": r[1], "detail": r[2], "status": r[3]}} for r in rows]

@app.post("/api/v1/{entity_plural}", response_model={primary_entity}Response)
def create_{entity_lower}(item: {primary_entity}Create):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO {entity_plural} (name, detail, status) VALUES (?, ?, ?)", 
                   (item.name, item.detail, item.status))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {{"id": item_id, "name": item.name, "detail": item.detail, "status": item.status}}

@app.get("/api/v1/{entity_plural}/{{item_id}}", response_model={primary_entity}Response)
def get_{entity_lower}_by_id(item_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, detail, status FROM {entity_plural} WHERE id = ?", (item_id,))
    r = cursor.fetchone()
    conn.close()
    if not r:
        raise HTTPException(status_code=404, detail="{primary_entity} not found")
    return {{"id": r[0], "name": r[1], "detail": r[2], "status": r[3]}}

@app.delete("/api/v1/{entity_plural}/{{item_id}}")
def delete_{entity_lower}(item_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {entity_plural} WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return {{"message": f"{primary_entity} deleted successfully"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

        # app/__init__.py
        files["app/__init__.py"] = '"""Application Package"""\n'

        # requirements.txt
        files["requirements.txt"] = "fastapi>=0.100.0\nuvicorn>=0.20.0\npydantic>=2.0.0\npytest>=7.0.0\nrequests>=2.28.0\n"

        return files

    def _generate_java_app(self, spec: TaskSpec, plan: ArchitecturePlan, output_dir: str) -> Dict[str, str]:
        files = {}
        files["pom.xml"] = """<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.app</groupId>
    <artifactId>student-api</artifactId>
    <version>1.0.0</version>
</project>"""
        files["src/main/java/com/app/Application.java"] = """package com.app;

public class Application {
    public static void main(String[] args) {
        System.out.println("Student Management Service Running");
    }
}"""
        return files

    def _generate_node_app(self, spec: TaskSpec, plan: ArchitecturePlan, output_dir: str) -> Dict[str, str]:
        files = {}
        files["package.json"] = '{\n  "name": "' + spec.project_name + '",\n  "version": "1.0.0",\n  "main": "src/server.js"\n}'
        files["src/server.js"] = 'const express = require("express");\nconst app = express();\napp.listen(8000, () => console.log("Server running on 8000"));'
        return files
