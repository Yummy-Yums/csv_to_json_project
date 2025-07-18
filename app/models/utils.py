from app.models.db import Transformation_Job, Transformation_Log
from sqlmodel import Session, select
from typing import Dict, Any, Union ,Optional
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timezone
from uuid import UUID

def create_job(
    filename: str, 
    filepath:str, 
    rules: Dict[Any, Any], 
    session: Session
) -> Transformation_Job:
    job = Transformation_Job(filename=filename, filepath=filepath, rules=rules)
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
    rules: Dict[Any, Any] | None,
    session: Session
) -> Transformation_Log:
    log = Transformation_Log(
        job_id=job_id,
        status=status,
        records_processed=records_processed,
        error_message=error_message,
        rules=rules
    )
    with session:
        session.add(log)
        session.commit()
        session.refresh(log)
        session.close()
    return log

def get_jobs(session: Session) -> list[Transformation_Job]:
    with session:
        jobs = session.exec(select(Transformation_Job)).all()
        session.close()
    return jobs

def get_job(job_id: Union[str, UUID], session: Session) -> Optional[Transformation_Job]:
    """Get a job by ID, handling both string and UUID inputs"""
    with session:
        job = session.get(Transformation_Job, str(job_id))
        session.close()
    return job

def get_job_log(job_id: Union[str, UUID], session: Session) -> Optional[Transformation_Log]:
    """Get a job log by ID, handling both string and UUID inputs"""
    with session:
        # Try direct lookup first
        log = session.exec(
            select(Transformation_Log)
            .where(Transformation_Log.job_id == str(job_id))
        ).first()
        session.close()
    return log

def check_file_exists(fileName: str):
    uploaded_files_folder = Path(__file__).parent.parent / "uploads"
    filepath = uploaded_files_folder.resolve() / fileName
    print(filepath)
    return filepath.exists()