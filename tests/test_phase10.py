import os
import pytest
from agent.phase10_delivery.packager import FinalDeliveryPackager

def test_phase10_delivery_packaging(tmp_path):
    packager = FinalDeliveryPackager()

    # Create dummy app directory structure
    app_dir = tmp_path / "sample_app"
    app_dir.mkdir()
    (app_dir / "main.py").write_text("print('hello')")
    (app_dir / "requirements.txt").write_text("fastapi")

    result = packager.package_delivery(str(app_dir))

    assert result["deployment_ready"] is True
    assert os.path.exists(result["release_archive"])
    assert os.path.exists(app_dir / "Dockerfile")
    assert os.path.exists(app_dir / "docker-compose.yml")
