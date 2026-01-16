from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_USER, PASSWORD, PORT, HOST, DATABASE

# Construction directe de l'URL sans encodage
# Attention : Si PASSWORD contient un '@', cette URL sera corrompue
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()