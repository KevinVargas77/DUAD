import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ENGINE_URL = "postgresql+psycopg2://postgres:12345@localhost/M2_Week6"
engine = create_engine(ENGINE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)