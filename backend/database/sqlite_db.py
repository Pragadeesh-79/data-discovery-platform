"""
SQLite database configuration for the DPDPA Data Discovery Platform.
This module handles creating the SQLAlchemy engine and managing DB sessions.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# 1. Define the SQLite database URL
# This tells SQLAlchemy to create a local file named "data_discovery.db"
# The "./" means it will be created in the root directory where main.py runs
DATABASE_URL = "sqlite:///./data_discovery.db"

# 2. Create the Database Engine
# The engine is the starting point for any SQLAlchemy application.
# It acts as a core interface to the database.
# `check_same_thread=False` is needed for SQLite to allow multiple FastAPI background requests to interact with it.
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 3. Create the Session Factory
# Sessions establish the actual conversations with the database.
# `autocommit=False` means we manually have to tell the DB to save changes (using db.commit()).
# `autoflush=False` gives us more control over when queries are executed.
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# 4. Create the Base Class
# Any python class that represents a Database Table must inherit this Base class.
# It tells SQLAlchemy "Hey, this class is a database table!"
Base = declarative_base()

# 5. Dependency Function (Bonus hook for FastAPI)
# This function creates an independent database session for each specific API request
# and ensures it safely closes automatically once the request is complete.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

