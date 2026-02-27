from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Helper for Docker vs Localhost
# If running in Docker container, host is 'db'. If running on Windows host, 'localhost'.
# localhost for development on Windows host.
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/nexatest"

# echo=True logs all SQL queries (good for debugging)
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Create all tables defined in SQLModel metadata"""
    SQLModel.metadata.create_all(engine)
