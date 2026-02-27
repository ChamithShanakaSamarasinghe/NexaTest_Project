from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from enum import Enum
from sqlalchemy import Column, JSON

class JobStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Job(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    status: JobStatus = Field(default=JobStatus.QUEUED)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    result: Optional[Dict] = Field(default=None, sa_column=Column(JSON))
    error: Optional[str] = Field(default=None)
    
    # Relationships
    documents: List["Document"] = Relationship(back_populates="job")

class Document(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    job_id: uuid.UUID = Field(foreign_key="job.id")
    
    filename: str
    content_type: str
    file_size_bytes: int = 0
    file_path: str
    extension: str # Used for parsing strategy
    sha256: str = Field(index=True) # For duplicate detection
    
    status: str = "uploaded" # uploaded, parsed, failed
    created_at: datetime = Field(default_factory=datetime.now)
    
    summary_text: Optional[str] = Field(default=None) # sa_column=Column(TEXT) in Postgres
    raw_json: Optional[Dict] = Field(default=None, sa_column=Column(JSON)) # For debugging
    
    # Relationships
    job: Job = Relationship(back_populates="documents")
    chunks: List["DocumentChunk"] = Relationship(back_populates="document")
    images: List["DocumentImage"] = Relationship(back_populates="document")
    tables: List["DocumentTable"] = Relationship(back_populates="document")
    keywords: List["DocumentKeyword"] = Relationship(back_populates="document")
    entities: List["DocumentEntity"] = Relationship(back_populates="document")

class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunks"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    
    chunk_index: int
    section_title: Optional[str] = None
    text: str # The content chunk
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    
    document: Document = Relationship(back_populates="chunks")

class DocumentImage(SQLModel, table=True):
    __tablename__ = "document_images"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    
    page_no: Optional[int] = None
    image_path: str
    caption: Optional[str] = None
    
    document: Document = Relationship(back_populates="images")

class DocumentTable(SQLModel, table=True):
    __tablename__ = "document_tables"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    
    page_no: Optional[int] = None
    table_json: Dict = Field(default={}, sa_column=Column(JSON))
    
    document: Document = Relationship(back_populates="tables")

class DocumentKeyword(SQLModel, table=True):
    __tablename__ = "document_keywords"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    
    keyword_text: str
    score: float
    source: str = "keybert-minilm"
    created_at: datetime = Field(default_factory=datetime.now)
    
    document: Document = Relationship(back_populates="keywords")

class DocumentEntity(SQLModel, table=True):
    __tablename__ = "document_entities"
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: uuid.UUID = Field(foreign_key="document.id")
    
    entity_text: str
    entity_label: str
    count: int = 1
    source: str = "spacy-en_core_web_sm"
    
    document: Document = Relationship(back_populates="entities")
