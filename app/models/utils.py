from app.models.db import Transformation_Job, Transformation_Log
from sqlmodel import Session, select
from typing import Dict, Any, Union ,Optional, Tuple, List
from uuid import uuid4
from pathlib import Path
from datetime import datetime, timezone
from uuid import UUID
from app.utils.logger import logger
import csv, json

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
    upload_files_folder = Path(__file__).parent.parent / "uploads"
    filepath = upload_files_folder.resolve() / fileName
    print(filepath)
    return filepath.exists()

def run_transformation_job(fileName: str, rules: Dict[Any, Any]):
    # check if fle exists
    # get file 
    # convert csv to json
    # apply rules
    # save json to downloads folder
    if not check_file_exists(fileName):
        raise FileNotFoundError(f"File {fileName} does not exist in the uploads folder.")
    
    upload_files_folder = Path(__file__).parent.parent / "uploads"
    csv_file_path = upload_files_folder / fileName
    success, json_file_path = csv_to_json(str(csv_file_path))

    if not success:
        raise Exception("Failed to convert CSV to JSON")
    
    file_path = Path(json_file_path)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        raise Exception(f"Failed to read JSON file: {e}")
    
    if isinstance(rules, str):
        try:
            rules = json.loads(rules)
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON in rules parameter: {e}")
    
    # Ensure rules is a dictionary
    if not isinstance(rules, dict):
        raise Exception("Rules must be a dictionary or valid JSON string")

    if not isinstance(rules, dict):
        raise Exception("Rules must be a dictionary or valid JSON string")
    
    transformed_data = data.copy()

    for rule_name, rule_config in rules.items():
        logger.info(f"Applying rule: {rule_name} with config: {json.dumps(rule_config)}")
        # Add more rules as needed

    # transform the data based on rules
    # field mapping
 
    for rule in rules:
        logger.info(str(json.dumps(rule)))
        if rule == "field_mappings":
            transformed_data = apply_field_mappings(transformed_data, rules[rule])
            # Add more rules as needed

    # If no rules or no records were transformed, keep original data
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(transformed_data, file, indent=4)
        
        logger.info(f"Transformation completed successfully. Output saved to: {json_file_path}")
        return str(json_file_path)
        
    except Exception as e:
        raise Exception(f"Failed to save transformed data: {e}")

def csv_to_json(file_path: str) -> Tuple[bool, str]:
    try:
        download_files_folder = Path(__file__).parent.parent / "downloads"
        download_files_folder.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            json_data = [row for row in reader]

        file_name = Path(file_path).stem 

        json_file_name = f"{file_name}.json"
        json_file_path = download_files_folder / json_file_name

        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        return (True, str(json_file_path))
    
    except Exception as e:
        logger.error(f"Error converting CSV to JSON: {e}")
        # Return False and the error message
        return (False, str(e))
    
def apply_field_mappings(data: List[Dict[str, Any]], mappings: Dict[str, str]) -> List[Dict[str, Any]]:
    """Apply field mapping transformations to the data."""
    transformed_data = []
    
    for record in data:
        new_record = record.copy()
        
        # Apply field mappings
        for old_field, new_field in mappings.items():
            if old_field in new_record:
                new_record[new_field] = new_record[old_field]
                if old_field != new_field:  # Only delete if names are different
                    del new_record[old_field]
        
        transformed_data.append(new_record)
        logger.debug(f"Transformed record: {new_record}")
    
    return transformed_data