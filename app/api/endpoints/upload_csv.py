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
    with open(uploaded_files_folder.resolve() / file.filename, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    return {"message": f"File {file.filename} uploaded successfully"}