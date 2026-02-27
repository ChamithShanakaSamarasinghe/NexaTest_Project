import uuid
import os
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".jpg", ".jpeg", ".png"}

def validate_file(file: UploadFile):
    # 1. Validate File Extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {ALLOWED_EXTENSIONS}")

    # 2. Validate File Size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Max 5MB.")
    
    return file_ext

def save_upload(file: UploadFile) -> dict:
    file_ext = validate_file(file)
    
    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    import hashlib
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "wb") as buffer:
            # Read in chunks to avoid memory issues and calc hash
            while chunk := file.file.read(4096):
                sha256_hash.update(chunk)
                buffer.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")

    file_size = os.path.getsize(file_path)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_path": file_path,
        "file_type": file_ext.replace(".", "").upper(),
        "extension": file_ext,
        "file_size_bytes": file_size,
        "sha256": sha256_hash.hexdigest(),
        "status": "UPLOADED"
    }
