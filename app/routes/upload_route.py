from fastapi import APIRouter, HTTPException, UploadFile, File
import shutil
import os
import uuid

router = APIRouter()

UPLOAD_DIR = "static/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"/{file_path}"
        return {"filename": unique_filename, "url": file_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image upload failed: {str(e)}")