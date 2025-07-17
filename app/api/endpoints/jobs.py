import json
from typing import Optional
from fastapi import APIRouter
from pathlib import Path
from app.models.db import *
from app.models.utils import *
from app.utils import logger

router = APIRouter(prefix="", tags=["Jobs Endpoints"])

@router.post("/transform-jobs")
async def create_transformation_job(job: Transformation_Job):
    if not job:
        return {"error": "No job data provided"}
    
    created_job = create_job(*job, session)
    if not created_job:
        return {"error": "Failed to create transformation job"}
    logger.info(f"Transformation job created: {created_job}")
    
    # create a log
    log = Transformation_Log(
        job_id=created_job.id,
        status="created",
        records_processed=0,
        error_message=None,
        rules=created_job.rules
    )

    log = create_log(*log, session)
    if not log:
        return {"error": "Failed to create transformation log"}
    logger.info(f"Transformation log created")
    return {
      "message": "Transformation job created successfully", 
      "job": created_job
    }

@router.get("/transform-jobs/{job_id}")
async def get_transformation_job(job_id: uuid4):
    if not job_id:
        return {"error": "No job ID provided"}
    
    job = get_job(job_id, session)
    if not job:
        return {"error": "Job not found"}
    
    log = get_job_log(job_id, session)
    if not log:
        return {"error": "Log not found for the job"}

    logger.info(f"Retrieved transformation job: {job}")
    
    return {
      "job": job,
    }

@router.get("/transform-jobs/")
async def get_transformation_jobs():
    
    jobs = get_jobs(session)
    if not jobs:
        return {"error": "No Jobs not found"}

    logger.info(f"Retrieving all transformation jobs")

    jobs_array = []

    for job in jobs:
        jobs_array.append({
            "id": job.id,
            "filename": job.filename,
            "filepath": job.filepath,
            "rules": job.rules,
            "created_at": job.created_at
        })
    
    return json.loads(jobs_array, default=str)