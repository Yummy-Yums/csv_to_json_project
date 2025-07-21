import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from main import app

from app.models.utils import csv_to_json, run_transformation_job

client = TestClient(app)


def test_create_transformation_job():

    success, error  = csv_to_json("users.csv")

    assert success is True