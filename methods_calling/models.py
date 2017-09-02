
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import create_engine, Column, String, DateTime



Base = declarative_base()

DB_ENGINE = create_engine('postgresql+psycopg2cffi://postgres:""@localhost/basesystem')

Session = sessionmaker(bind=DB_ENGINE)
session = Session()

class Jobs(Base):

    __tablename__ = "jobs"

    job_id = Column(String(43), nullable=False, primary_key=True)
    job_name = Column(String(32), nullable=False)
    created_at = Column(DateTime, server_default=func.timezone('UTC', func.current_timestamp()))
    updated_at = Column(DateTime, onupdate=func.timezone('UTC', func.current_timestamp()))

