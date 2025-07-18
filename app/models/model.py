# from sqlmodel import Field, SQLModel, JSON
# from datetime import datetime, timezone
# from typing import Dict, Any, Optional
# from uuid import UUID, uuid4
# import sqlalchemy as sa

# def utc_now():
#     return datetime.now(timezone.utc)

# class Transformation_Job(SQLModel, table=True):
#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     filename: str
#     filepath: str
#     rules: Optional[str] = Field(default=None, sa_type=sa.Text)
#     created_at: datetime = Field(default_factory=utc_now)

# class Transformation_Log(SQLModel, table=True):
#     id: UUID = Field(default_factory=uuid4, primary_key=True)
#     job_id: int = Field(foreign_key="transformation_job.id", sa_type=sa.UUID)
#     status: str = Field(default="pending")
#     records_processed: int 
#     error_message: str
#     rules: Optional[str] = Field(default=None, sa_type=sa.Text)
#     completed_at: datetime = Field(default_factory=utc_now)