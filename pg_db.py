import databases
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_DB_NAME  = os.environ['POSTGRES_DB_NAME']
POSTGRES_DB_USER_NAME  = os.environ['POSTGRES_DB_USER_NAME']
POSTGRES_DB_USER_PASSWORD  = os.environ['POSTGRES_DB_USER_PASSWORD']
POSTGRES_DB_PORT  = os.environ['POSTGRES_DB_PORT']
POSTGRES_DB_HOST  = os.environ['POSTGRES_DB_HOST']


DATABASE_URL = f"postgresql://{POSTGRES_DB_USER_NAME}:{POSTGRES_DB_USER_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

