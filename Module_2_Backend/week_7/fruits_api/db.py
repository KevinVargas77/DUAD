# Database connection and setup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from config import settings
from models import Base

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=settings.SQL_ECHO)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

# Function to create all tables in the database
def init_db():
    Base.metadata.create_all(bind=engine)
