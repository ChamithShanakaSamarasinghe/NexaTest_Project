from sqlmodel import Session, select
from app.core.database import engine
from app.models.sql_models import (
    Job, Document, JobStatus, 
    DocumentChunk, DocumentImage, DocumentTable, 
    DocumentEntity, DocumentKeyword
)
from datetime import datetime
import uuid
from typing import Optional, List, Dict

class PostgresJobStore:
    def create_job(self, job: Job) -> Job:
        with Session(engine) as session:
            session.add(job)
            session.commit()
            session.refresh(job)
            return job

    def create_document(self, doc: Document) -> Document:
        with Session(engine) as session:
            session.add(doc)
            session.commit()
            session.refresh(doc)
            return doc

    def get_job(self, job_id: uuid.UUID | str) -> Optional[Job]:
        with Session(engine) as session:
            if isinstance(job_id, str):
                try:
                    job_id = uuid.UUID(job_id)
                except ValueError:
                    return None
            return session.get(Job, job_id)

    def update_job(self, job: Job) -> Job:
        with Session(engine) as session:
            db_job = session.get(Job, job.id)
            if db_job:
                db_job.status = job.status
                db_job.result = job.result # Optional result blob
                db_job.error = job.error # Optional error
                db_job.updated_at = datetime.now()
                session.add(db_job)
                session.commit()
                session.refresh(db_job)
                return db_job
            return job

    def get_document_by_hash(self, sha256: str) -> Optional[Document]:
        with Session(engine) as session:
            statement = select(Document).where(Document.sha256 == sha256)
            return session.exec(statement).first()

    def get_job_document(self, job_id: uuid.UUID | str) -> Optional[Document]:
        if isinstance(job_id, str):
            try:
                job_id = uuid.UUID(job_id)
            except ValueError:
                return None
                
        with Session(engine) as session:
            statement = select(Document).where(Document.job_id == job_id)
            return session.exec(statement).first()

    def save_enrichment_results(self, 
                                doc_id: uuid.UUID, 
                                summary: str, 
                                chunks: List[Dict],
                                images: List[Dict], # {page_no, image_path, caption}
                                tables: List[Dict], # {page_no, table_json}
                                keywords: List[Dict], 
                                entities: List[Dict]):
        with Session(engine) as session:
            doc = session.get(Document, doc_id)
            if not doc:
                return
            
            # Update Document Summary & Status
            doc.summary_text = summary
            doc.status = "parsed"
            session.add(doc)
            
            # 1. Chunks
            for c in chunks:
                db_chunk = DocumentChunk(
                    document_id=doc_id,
                    chunk_index=c.get("chunk_index", 0),
                    text=c.get("text", ""),
                    section_title=c.get("section_title"),
                    page_start=c.get("page_start"),
                    page_end=c.get("page_end")
                )
                session.add(db_chunk)

            # 2. Images
            for img in images:
                # Expecting path, page, caption
                # If image_path is null (from docling failing to save?), skip or handle?
                if img.get("image_path"):
                    db_img = DocumentImage(
                        document_id=doc_id,
                        page_no=img.get("page_no"),
                        image_path=img.get("image_path"),
                        caption=img.get("caption")
                    )
                    session.add(db_img)

            # 3. Tables
            for tbl in tables:
                # Expecting page_no, data
                db_tbl = DocumentTable(
                    document_id=doc_id,
                    page_no=tbl.get("page_no"),
                    table_json=tbl.get("data", {}) # docling returns 'data' usually
                )
                session.add(db_tbl)
            
            # 4. Keywords
            for kw in keywords:
                db_kw = DocumentKeyword(
                    document_id=doc_id, 
                    keyword_text=kw.get("text"), 
                    score=kw.get("score", 0.0),
                    source="keybert"
                )
                session.add(db_kw)
            
            # 5. Entities
            for ent in entities:
                db_ent = DocumentEntity(
                    document_id=doc_id, 
                    entity_text=ent.get("text"), 
                    entity_label=ent.get("label"),
                    count=ent.get("count", 1), # Default 1 if not provided
                    source="spacy"
                )
                session.add(db_ent)
                
            session.commit()

# Singleton
job_store = PostgresJobStore()
