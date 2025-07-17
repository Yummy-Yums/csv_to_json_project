from typing import Optional
from fastapi import APIRouter, UploadFile
from pathlib import Path

router = APIRouter(prefix="/upload", tags=["Upload File Endpoint"])

@router.post("/file")
async def create_upload_file(file: Optional[UploadFile] = None):
    if not file:
        return {"error": "No file provided"}
    elif not file.filename.endswith('.csv'):
        return {"error": "File is not a CSV"}
    res = await _save_uploaded_file(file)
    return res

async def _save_uploaded_file(file: UploadFile):
    uploaded_files_folder = Path(__file__).parent.parent.parent / "uploads" 
    filepath = uploaded_files_folder.resolve() / file.filename

    if not uploaded_files_folder.exists():
        uploaded_files_folder.mkdir(parents=True, exist_ok=True)
    elif filepath.exists():
            return {"error": f"File {file.filename} already exists"}
    
    with open(filepath, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    return {"message": f"File {file.filename} uploaded successfully"}