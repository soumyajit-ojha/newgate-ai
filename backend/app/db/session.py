from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from decouple import config
from urllib import parse
# from app.core.config import settings

# Kleppmann: Connection pooling is handled by SQLAlchemy/Psycopg2 here
SUPABASE_URL_STR = str(config("SUPABASE_URL")).split("/")[-1]
SUPABASE_DB_PASSWORD = parse.quote_plus(config("SUPABASE_DB_PASSWORD"))
DATABASE_URL = f"postgresql://postgres:{SUPABASE_DB_PASSWORD}@db.{SUPABASE_URL_STR}:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()