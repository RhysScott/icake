from fastapi import APIRouter, UploadFile, File
import os
from utils import ApiResponse

router = APIRouter(prefix='/common')

@router.post("/upload")
def upload(files: list[UploadFile] = File(...)):
    os.makedirs("upload/files", exist_ok=True)
    filenames = []
    for file in files:
        filename = file.filename or "unknown"
        save_path = f"upload/files/{filename}"
        with open(save_path, "wb") as f:
            f.write(file.file.read())
        filenames.append(filename)
    return ApiResponse.success(data={"filenames": filenames})
