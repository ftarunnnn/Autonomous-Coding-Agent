import os
import shutil
import zipfile
import subprocess
from typing import Dict, Any, Optional

class FinalDeliveryPackager:
    """
    Phase 10 Module: Packages final working source code, tests, documentation,
    creates release archives, Docker deployment manifests, and git release commits.
    """

    def package_delivery(self, project_dir: str, archive_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Bundles the project into a release package (ZIP archive + Docker setup).
        """
        if not archive_name:
            archive_name = os.path.basename(os.path.normpath(project_dir)) + "_release.zip"

        # 1. Generate Dockerfile & docker-compose.yml
        self._generate_docker_manifests(project_dir)

        # 2. Create ZIP Archive
        archive_path = os.path.join(os.path.dirname(project_dir) or ".", archive_name)
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_dir)
                    zipf.write(file_path, arcname)

        return {
            "project_directory": project_dir,
            "release_archive": archive_path,
            "deployment_ready": True,
            "manifests": ["Dockerfile", "docker-compose.yml", "README.md", "API_DOCS.md", "ARCHITECTURE.md"]
        }

    def _generate_docker_manifests(self, project_dir: str):
        dockerfile = """FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
"""
        docker_compose = """version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - PORT=8000
"""
        with open(os.path.join(project_dir, "Dockerfile"), "w", encoding="utf-8") as f:
            f.write(dockerfile)

        with open(os.path.join(project_dir, "docker-compose.yml"), "w", encoding="utf-8") as f:
            f.write(docker_compose)
