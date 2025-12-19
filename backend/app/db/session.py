from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config
from urllib import parse

# from app.core.config import settings
RDS_ENDPOINT = config("RDS_ENDPOINT")
RDS_USER = config("RDS_USER")
RDS_PASSWORD = parse.quote_plus(config("RDS_PASSWORD"))
DATABASE_URL = f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_ENDPOINT}:3306/newgate"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
