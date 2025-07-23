

# FastAPI CSV Transformation Service

A FastAPI-based service for uploading, transforming, and downloading CSV files with customizable transformation rules.

Read More at DeepWiki

[DeepWiki](https://deepwiki.com/badge-maker?url=https%3A%2F%2Fdeepwiki.com%2FYummy-Yums%2Fcsv_to_json_project)

## Project Summary

This service allows users to:
- Upload CSV files
- Create transformation jobs with custom rules
- Transform CSV files based on specified rules
- Download transformed files
- Track transformation job status and logs

## Project Structure

```
fastapi-playground/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── jobs.py         # Job-related endpoints
│   │   │   └── upload_csv.py   # File upload endpoints
│   │   └── healthcheck.py
│   ├── models/
│   │   ├── db.py              # Database models and config
│   │   ├── model.py           # SQLModel definitions
│   │   └── utils.py           # Database utility functions
│   ├── tests/
│   │   ├── test_jobs_endpoint.py
│   │   └── test_upload_csv.py
│   ├── utils/
│   │   └── logger.py          # Logging configuration
│   ├── downloads/             # Transformed files storage
│   └── uploads/              # Uploaded files storage
├── main.py                   # FastAPI application entry point
└── README.md
```

## Technology Stack

- **FastAPI**: Web framework for building APIs
- **SQLModel**: SQL database interaction
- **SQLite**: Database engine
- **Python 3.10+**: Programming language
- **pytest**: Testing framework
- **httpie**: HTTP client for testing

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd into folder
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
uvicorn main:app --reload
```

## API Endpoints

### 1. Upload CSV File
```bash
# Upload a CSV file
http --form POST :8000/upload/file file@users.csv
```

### 2. Create Transformation Job
```bash
# Simple transformation
http POST :8000/transform-jobs filename=test.csv rules:='{"some": "rule"}'

# Field mapping transformation
http POST :8000/transform-jobs \
  filename=users.csv \
  rules:='{
    "field_mappings": {
      "firstName": "first_name",
      "lastName": "last_name",
      "emailAddress": "email",
      "createdAt": "created_date"
    }
  }'
```

### 3. Get Job Status
```bash
# Get status of a specific job
http :8000/transform-jobs/{job_id}/status
```

### 4. List All Jobs
```bash
# Get all transformation jobs
http :8000/transform-jobs/

test@pop-os:~/Desktop$ http GET :8000/transform-jobs/
HTTP/1.1 200 OK
content-length: 11857
content-type: application/json
date: Wed, 23 Jul 2025 10:37:26 GMT
server: uvicorn

[
    {
        "created_at": "2025-07-22T11:58:25.996966",
        "filename": "test_file.csv",
        "filepath": "uploads/test_file.csv",
        "id": "933b2157-d8ee-4075-b076-3978eb2c2db7",
        "rules": {
            "column": "age",
            "operation": "multiply",
            "value": 2
        }
    },
    {
        "created_at": "2025-07-22T11:58:26.055447",
        "filename": "test_file.csv",
        "filepath": "uploads/test_file.csv",
        "id": "27fa371c-f3ed-491e-b06c-a9f372eea5a7",
        "rules": {
            "column": "age",
            "operation": "multiply",
            "value": 2
        }
    },
    ....
]
```

### 5. Download Transformed File
```bash
# Download a transformed file
http :8000/transform-jobs/{filename}/download
```

## Example Workflow

1. Upload a CSV file:
```bash
http --form POST :8000/upload/file file@users.csv

test@pop-os:~/Desktop$ http --form POST :8000/upload/file file@users.csv
HTTP/1.1 200 OK
content-length: 41
content-type: application/json
date: Wed, 23 Jul 2025 10:45:04 GMT
server: uvicorn

{
    "error": "File users.csv already exists"
}


```

2. Create a transformation job:
```bash
http POST :8000/transform-jobs \
  filename=users.csv \
  rules:='{
    "field_mappings": {
      "firstName": "first_name",
      "lastName": "last_name"
    }
  }'

test@pop-os:~/Desktop$ http POST :8000/transform-jobs   filename=users.csv   rules:='{"field_mappings": {"firstName": "first_name", "lastName": "last_name", "emailAddress": "email", "createdAt": "created_date"}}'
HTTP/1.1 200 OK
content-length: 356
content-type: application/json
date: Wed, 23 Jul 2025 10:42:11 GMT
server: uvicorn

{
    "job": {
        "created_at": "2025-07-23T10:42:12.025685",
        "filename": "users.csv",
        "filepath": "uploads/users.csv",
        "id": "471030d4-478d-4701-bf26-591a4c12e313",
        "rules": "{\"field_mappings\": {\"firstName\": \"first_name\", \"lastName\": \"last_name\", \"emailAddress\": \"email\", \"createdAt\": \"created_date\"}}"
    },
    "message": "Transformation job created successfully"
}


```

3. Check job status:
```bash
http :8000/transform-jobs/{returned_job_id}/status

test@pop-os:~/Desktop$ http GET :8000/transform-jobs/933b2157-d8ee-4075-b076-3978eb2c2db7/status
HTTP/1.1 200 OK
content-length: 263
content-type: application/json
date: Wed, 23 Jul 2025 10:40:01 GMT
server: uvicorn

{
    "job": {
        "completed_at": "2025-07-22T11:58:26.025120",
        "error_message": "",
        "id": "36d3c4d5-1a91-4598-b1c8-1705b77ca14f",
        "job_id": "933b2157-d8ee-4075-b076-3978eb2c2db7",
        "records_processed": 0,
        "rules": {
            "column": "age",
            "operation": "multiply",
            "value": 2
        },
        "status": "created"
    }
}
```

4. Download transformed file:
```bash
test@pop-os:~/Desktop$ http :8000/transform-jobs/test_file.json/download > transfomred_file.json

```

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/test_jobs_endpoint.py -v
```

## License

MIT
