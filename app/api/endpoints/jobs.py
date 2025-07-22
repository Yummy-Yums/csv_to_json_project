import json
from typing import Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from app.models.db import Transformation_Job, Transformation_Log
from app.models.utils import *
from app.utils.logger import logger
from uuid import UUID
from app.models.db import get_session

router = APIRouter(prefix="", tags=["Jobs Endpoints"])

# use a Response Model for the job creation
session = get_session()

class RequestJobCreate(BaseModel):
    filename: str
    rules: Optional[Dict[Any, Any]] = None

@router.post("/transform-jobs")
async def create_transformation_job(job: RequestJobCreate):
    if not job:
        return {"error": "No data was sent"}
    
    if not check_file_exists(job.filename, "uploads"):
        return {"error": f"File {job.filename} has not been uploaded yet, You need to uplaod the file first before creating the job"}
    
    created_job = create_job(
        filename=job.filename,
        filepath=str(Path("uploads") / job.filename),
        rules=json.dumps(job.rules),
        session=session
    )

    if not created_job:
        return {"error": "Failed to create transformation job"}
    
    logger.info(f"Transformation job created: {created_job}")
    
    # create a log
    log = Transformation_Log(
        job_id=created_job.id,
        status="created",
        records_processed=0,
        rules=created_job.rules
    )

    log = create_log(
        job_id=created_job.id,
        status=log.status,
        records_processed=log.records_processed,
        error_message=log.error_message,
        rules=json.loads(log.rules),
        session=session
    )

    if not log:
        return {"error": "Failed to create transformation log"}
    
    logger.info(f"Transformation log created")

    return {
      "message": "Transformation job created successfully", 
      "job": created_job
    }

@router.get("/transform-jobs/{job_id}")
async def get_transformation_job(job_id: UUID):

    try:
        job = get_job(job_id, session)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # return a properly formatted response
        return {"job": job}
    finally:
        session.close()

@router.get("/transform-jobs/{job_id}/status")
async def get_transformation_job_status(job_id: UUID):

    try:
        log = get_job_log(job_id, session)
        if not log:
            raise HTTPException(status_code=404, detail="Job Log not found")
        
        # return a properly formatted response
        return {"job": log}
    finally:
        session.close()

@router.get("/transform-jobs/")
async def get_all_jobs():
    try:
        jobs = get_jobs(session)
        if not jobs:
            return []

        logger.info(f"Retrieving all transformation jobs")

        jobs_array = []

        for job in jobs:
            jobs_array.append({
                "id": str(job.id),
                "filename": job.filename,
                "filepath": job.filepath,
                "rules": json.loads(job.rules),
                "created_at": job.created_at.isoformat() if job.created_at else None
            })
        
        return jobs_array
    finally:
        session.close()

# get job status 

@router.post("/transform-jobs/{job_id}/run")
async def run_transformation_job_endpoint(job_id: UUID):

    try:
        job = get_job(job_id, session)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        check_file_exists(job.filename, "uploads")
        
        run_transformation_job(job.filename, job.rules)

        create_log(
            job_id=job.id,
            status="completed",
            records_processed=1,  # This should be updated based on actual processing
            error_message="",
            rules=json.loads(job.rules),
            session=session
        )
    
        # return a properly formatted response
        return {"job": job}
    except Exception as e:
        logger.error(f"Error running transformation job: {e}")
        raise HTTPException(status_code=500, detail="Failed to run transformation job")
    finally:
        session.close()

# download job results
@router.get("/transform-jobs/{filename}/download")
async def download_transformation_job(filename: str):
       
        if not check_file_exists(filename, "downloads"):
            raise HTTPException(status_code=404, detail=f"File {filename} not found ")
        
        download_files_folder_path = Path(__file__).parent.parent.parent / "downloads"
        
        file_path = download_files_folder_path / filename
        # /home/test/Desktop/python/fastapi/playground/app/downloads/users.json

        print(file_path)
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail=f"File {filename} does not exist")
        
        return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
