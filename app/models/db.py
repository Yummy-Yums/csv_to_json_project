from sqlmodel import Field, Session, SQLModel, create_engine, text
from pathlib import Path
# from app.models.utils import *
from typing import Optional

from sqlmodel import Field, SQLModel, JSON
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
import sqlalchemy as sa

# Database configuration
DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    return Session(engine)

def create_db_and_tables():
    db_path = Path("database.db")
    if not db_path.exists():
        print("Database does not exist. Creating database and tables...")
        try:
            SQLModel.metadata.create_all(engine)
            print("Database tables created successfully")
        except Exception as e:
            print(f"An error occurred while creating the database: {e}")
    else:
        print("Database already exists. No need to create tables.")

def utc_now():
    return datetime.now(timezone.utc)

class Transformation_Job(SQLModel, table=True):
    __tablename__ = "transformation_job"

    id: str = Field(
        default_factory=lambda: str(uuid4()), 
        primary_key=True, 
        sa_type=sa.String(36)
    )
    filename: str
    filepath: str
    rules: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_type=sa.JSON()  # Use JSON type for dictionaries
    )
    created_at: datetime = Field(default_factory=utc_now)

class Transformation_Log(SQLModel, table=True):
    __tablename__ = "transformation_log"

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        sa_type=sa.String(36)  # Store as string in SQLite
    )
    job_id: str = Field(
        sa_type=sa.String(36),  # Changed from int to UUID
        foreign_key="transformation_job.id"
    )
    status: str = Field(default="pending")
    records_processed: int = Field(default=0)
    error_message: str = Field(default="")
    rules: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_type=sa.JSON()  # Use JSON type for dictionaries
    )
    completed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )