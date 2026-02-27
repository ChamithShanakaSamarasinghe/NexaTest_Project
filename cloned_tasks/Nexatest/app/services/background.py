from app.services.storage import job_store
from app.models.sql_models import JobStatus
from app.services.parsing.orchestrator import Orchestrator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

orchestrator = Orchestrator()

def process_document_job(job_id: str):
    """
    Background worker function to process the document.
    Runs in a threadpool (because it's a sync function).
    """
    logger.info(f"Starting job {job_id}")
    job = job_store.get_job(job_id)
    if not job:
        logger.error(f"Job {job_id} not found")
        return

    try:
        # Update status to PROCESSING
        job.status = JobStatus.PROCESSING
        job_store.update_job(job)

        # Get Document info from DB
        doc = job_store.get_job_document(job.id)
        if not doc:
            raise ValueError("No document associated with this job.")

        # Run Orchestrator
        # process method expects (job_id, file_path, file_type)
        logger.info(f"Processing file: {doc.file_path}")
        result = orchestrator.process(str(job.id), doc.file_path, doc.extension)
        
        # Extract Results
        content = result.get("content", {})
        enrichment = result.get("enrichment", {})
        
        summary = enrichment.get("summary", "")
        features = enrichment.get("features", {})
        
        chunks = features.get("chunks", [])
        keywords = features.get("keywords", [])
        entities = features.get("entities", [])
        
        # From content (Docling output)
        images = content.get("images", []) # List of {image_path, ...}
        tables = content.get("tables", []) # List of {data, ...}
        
        # Save to DB
        job_store.save_enrichment_results(
            doc_id=doc.id,
            summary=summary,
            chunks=chunks,
            images=images,
            tables=tables,
            keywords=keywords,
            entities=entities
        )
        
        # Update Job Status
        job.status = JobStatus.COMPLETED
        job_store.update_job(job)
        logger.info(f"Job {job_id} completed successfully.")
        
    except Exception as e:
        logger.exception(f"Job {job_id} failed: {e}")
        print(f"CRITICAL ERROR in JOB {job_id}: {e}") # Print for immediate visibility
        job.status = JobStatus.FAILED
        job.error = str(e)
        job_store.update_job(job)


