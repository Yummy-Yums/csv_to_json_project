# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_valid_csv_file_upload():
    # Test uploading a valid CSV file
    with open("test_file.csv", "w") as f:
        f.write("name,age\nAlice,30\nBob,25")
    
    with open("test_file.csv", "rb") as file:
        response = client.post("/upload/file", files={"file": ("test_file.csv", file, "text/csv")})
    
    assert response.status_code == 200
    assert response.json() == {"message": "File test_file.csv uploaded successfully"}

def test_non_csv_file_upload():
    # Test uploading a non-CSV file
    with open("test_file.txt", "w") as f:
        f.write("This is a text file.")
    
    with open("test_file.txt", "rb") as file:
        response = client.post("/upload/file", files={"file": ("test_file.txt", file, "text/plain")})
    
    assert response.status_code == 200
    assert response.json() == {"error": "File is not a CSV"}

def test_no_file_upload():
    # Test uploading without a file
    response = client.post("/upload/file")
    
    assert response.status_code == 200
    assert response.json() == {"error": "No file provided"}