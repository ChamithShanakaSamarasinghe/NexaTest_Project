from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.services import ingestion, storage, background
from app.models.sql_models import Job, Document, JobStatus
import uuid

router = APIRouter()

@router.post("/upload")
def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 1. Save File
    file_info = ingestion.save_upload(file)
    
    # 1.5 Check Deduplication
    existing_doc = storage.job_store.get_document_by_hash(file_info["sha256"])
    if existing_doc:
        # Return existing job info
        # Optionally fetch current status , For simple return:
        return {
            "job_id": str(existing_doc.job_id),
            "status": "ALREADY_EXISTS",
            "message": "File already processed. Returning existing job."
        }

    # 2. Create Job
    job = Job(status=JobStatus.QUEUED)
    storage.job_store.create_job(job)
    
    # 3. Create Document
    doc = Document(
        job_id=job.id,
        filename=file_info["filename"],
        file_path=file_info["file_path"],
        content_type=file_info["file_type"],
        extension=file_info["extension"],
        file_size_bytes=file_info["file_size_bytes"],
        sha256=file_info["sha256"],
        status="uploaded"
    )
    storage.job_store.create_document(doc)

    # 4. Trigger Background Task
    background_tasks.add_task(background.process_document_job, str(job.id))

    return {"job_id": str(job.id), "status": "QUEUED"}

@router.get("/jobs/{job_id}")
def get_job_status(job_id: str):
    try:
        j_uuid = uuid.UUID(job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID")
        
    job = storage.job_store.get_job(j_uuid)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
