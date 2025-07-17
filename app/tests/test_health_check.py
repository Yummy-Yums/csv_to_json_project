import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/health_check")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_database_creation():
    # Assuming the database creation function is called during startup, check in the directory 
    db_path = "database.db"
    assert os.path.exists(db_path), "Database file should exist after startup"
   