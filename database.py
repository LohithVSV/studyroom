from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()   #loads environment variables from .env file

DATABASE_URL=os.environ.get("DATABASE_URL")       #connects to database

engine=create_engine(DATABASE_URL)   #creates a database engine

Base=declarative_base() 

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
