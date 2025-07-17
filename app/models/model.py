from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Dict, Any
import uuid

class Transformation_Job(SQLModel, table=True):
    id: int = Field(default=uuid.uuid4, primary_key=True)
    filename: str
    filepath: str
    rules: Dict[Any, Any] | None = None
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))

class Transformation_Log(SQLModel, table=True):
    id: int = Field(default=uuid.uuid4, primary_key=True)
    job_id: int = Field(foreign_key="transformation_job.id")
    status: str = Field(default="pending")
    records_processed: int 
    error_message: str = None
    rules: Dict[Any, Any]
    completed_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))