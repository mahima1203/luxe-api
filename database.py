from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Example connection string: postgresql://username:password@localhost:5432/luxedb
# For testing or before setting up, you can fallback to sqlite
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./luxe.db")

# 🛠️ ADVANCED AUTO-FIX: Handle messy clipboard/copy-paste issues
if SQLALCHEMY_DATABASE_URL:
    # 1. Remove accidental spaces
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.strip()
    
    # 2. If the user mistakenly pasted "DATABASE_URL=...", remove that prefix
    if SQLALCHEMY_DATABASE_URL.startswith("DATABASE_URL="):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL[13:].strip()
    
    # 3. Handle 'postgres://' vs 'postgresql://'
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # 🛠️ DEBUGGING: This will help us see what is happening in Render logs
    # (We hide the sensitive password for safety)
    safe_info = SQLALCHEMY_DATABASE_URL[:15] + "..." if len(SQLALCHEMY_DATABASE_URL) > 15 else "Empty/Short"
    print(f"DATABASE_CONNECTION: Trying to connect with prefix: {safe_info}")

# SQLite needs connect_args={"check_same_thread": False}, Postgres doesn't
options = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=options
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
