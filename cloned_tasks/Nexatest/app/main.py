from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="Nexatest Document Ingestion API", version="1.0.0")

app.include_router(endpoints.router, prefix="/api/v1")

from app.core.database import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def run_health_check():
    return {"status": "ok", "message": "Nexatest API is running"}
