from app.models.db import Transformation_Job, Transformation_Log
from sqlmodel import Session
from typing import Dict, Any
from uuid import uuid4

def create_job(
    filename: str, 
    filepath:str, 
    rules: Dict[Any, Any], 
    session: Session
) -> Transformation_Job:
    job = Transformation_Job(filename, filepath, rules)
    with session:
        session.add(job)
        session.commit()
        session.refresh(job)
        session.close()
    return job

def create_log(
    job_id: uuid4,
    status: str,
    records_processed: int,
    error_message: str,
    rules: Dict[Any, Any],
    session: Session
) -> Transformation_Log:
    log = Transformation_Log(
        job_id,
        status,
        records_processed,
        error_message,
        rules
    )
    with session:
        session.add(log)
        session.commit()
        session.refresh(log)
        session.close()
    return log

def get_jobs(session: Session) -> list[Transformation_Job]:
    with session:
        jobs = session.exec(Transformation_Job.select()).all()
        session.close()
    return jobs

def get_job(job_id: int, session: Session) -> Transformation_Job:
    with session:
        job = session.get(Transformation_Job, job_id)
        session.close()
    return job

def get_job_log(job_id: int, session: Session) -> Transformation_Log:
    with session:
        log = session.get(Transformation_Log, job_id)
        session.close()
    return log