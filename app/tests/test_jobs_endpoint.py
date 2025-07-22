from uuid import uuid4
from pathlib import Path
from fastapi.testclient import TestClient
from main import app
from app.models.db import get_session

client = TestClient(app)
session = get_session()

def setup_test_data():
    """Helper function to setup test data"""
    # Create a test CSV file
    with open("test_file.csv", "w") as f:
        f.write("name,age\nAlice,30\nBob,25")
    
    # Upload the file
    with open("test_file.csv", "rb") as file:
        response = client.post("/upload/file", 
            files={"file": ("test_file.csv", file, "text/csv")}
        )
    
    # Create a test job
    job_data = {
        "filename": "test_file.csv",
        "rules": {"column": "age", "operation": "multiply", "value": 2}
    }
    response = client.post("/transform-jobs", json=job_data)
    return response.json()["job"]["id"]

def test_create_job():
    """Test job creation endpoint"""
    job_data = {
        "filename": "test_file.csv",
        "rules": {"column": "age", "operation": "multiply", "value": 2}
    }
    response = client.post("/transform-jobs", json=job_data)
    
    assert response.status_code == 200
    assert "job" in response.json()
    assert response.json()["job"]["filename"] == "test_file.csv"
    assert "id" in response.json()["job"]

def test_get_job():
    """Test getting a specific job"""
    # First create a job
    job_id = setup_test_data()
    
    # Then try to get it
    response = client.get(f"/transform-jobs/{job_id}")
    
    assert response.status_code == 200
    assert response.json()["job"]["id"] == job_id
    assert "filename" in response.json()["job"]
    assert "rules" in response.json()["job"]

def test_get_all_jobs():
    """Test getting all jobs"""
    response = client.get("/transform-jobs/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    if len(response.json()) > 0:
        assert "id" in response.json()[0]
        assert "filename" in response.json()[0]

def test_download_transformed_file():
    """Test downloading a transformed file"""
    # First create a job and transform
    setup_test_data()
    
    # Then try to download it
    response = client.get(f"/transform-jobs/test_file.json/download")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"
    assert "content-disposition" in response.headers

def test_get_nonexistent_job():
    """Test getting a job that doesn't exist"""
    id = uuid4()
    response = client.get(f"/transform-jobs/{id}")
    assert response.status_code == 404

def test_download_nonexistent_file():
    """Test downloading a file that doesn't exist"""
    response = client.get("/download/nonexistent-id")
    assert response.status_code == 404

def teardown_module():
    """Cleanup after tests while preserving folder structure"""
    # List of test files to cleanup
    test_files = [
        "test_file.csv",
        "test_file_transformed.csv",
    ]
    
    # Clean up test files from downloads directory
    downloads_path = Path(__file__).parent.parent / "downloads"
    for test_file in test_files:
        test_file_path = downloads_path / test_file
        if test_file_path.exists():
            test_file_path.unlink()
        
        # Also check current directory
        current_file_path = Path(__file__).parent.parent.parent / test_file
        if current_file_path.exists():
            current_file_path.unlink()
            
    print("Test cleanup complete - removed test files while preserving directories")