from sqlmodel import Field, Session, SQLModel, create_engine, text
from pathlib import Path
from utils import *
from model import Transformation_Job, Transformation_Log

def create_db_and_tables():
    db_path = Path("database.db")
    if not db_path.exists():
        print("Database does not exist. Creating database and tables...")
        try:
            engine = create_engine("sqlite:///database.db", echo=True)
            SQLModel.metadata.create_all(engine)
        except Exception as e:
            print(f"An error occurred while creating the database: {e}")
    else:
        print("Database already exists. No need to create tables.")

engine = create_engine("sqlite:///database.db", echo=True)
session = Session(engine)

# create_db_and_tables()
# create_heroes()
# read_heroes()
# delete_heroes()