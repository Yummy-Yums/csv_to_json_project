import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import shutil
from main import app
from app.utils.logger import logger

client = TestClient(app)

def setup_module():
    """Setup test environment"""
    # Create downloads directory if it doesn't exist
    downloads_path = Path(__file__).parent.parent / "downloads"
    downloads_path.mkdir(exist_ok=True)
    
    # Create a test file in downloads directory
    test_file = downloads_path / "test_file.csv"
    with open(test_file, "w") as f:
        f.write("name,age\nAlice,30\nBob,25")

def test_download_existing_file():
    """Test downloading an existing file"""
    response = client.get("/transform-jobs/test_file.csv/download")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert response.headers["content-disposition"] == 'attachment; filename="test_file.csv"'
    
    # Check content
    content = response.content.decode()
    assert "name,age" in content
    assert "Alice,30" in content

def test_download_nonexistent_file():
    """Test downloading a file that doesn't exist"""
    response = client.get("/transform-jobs/nonexistent.csv/download")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "File nonexistent.csv not found "}

def test_download_file_outside_downloads():
    """Test attempting to download a file outside downloads directory"""
    response = client.get("/transform-jobs/../secret.txt/download")
    
    assert response.status_code == 404


# def teardown_module():
#     """Cleanup test environment"""
#     # Remove test downloads directory and its contents
#     downloads_path = Path(__file__).parent.parent / "downloads"
#     if downloads_path.exists():
#         shutil.rmtree(downloads_path)
#     logger.info("Test cleanup complete")