# we want to connect our fastapi project to postgres database using sqlalchemy

from sqlalchemy import create_engine 
# create_engine is used to connect your code to actual database.
from sqlalchemy.orm import sessionmaker , declarative_base , Session
# sessionmaker ---> helps to create database session, like opening a connection to do queries.
# declarative_base ---> a base class that all models inherits from -- it required to let sqlalchemy know "these are my database tables."
from dotenv import load_dotenv
# loads variables from .env file.
import os
# read system and environment variables.

# loads the .env file into environment so os.getenv() can access it.
load_dotenv()

# Create database connection URL from environment variables
DATABASE_URL = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# create a SQLALchemy engine
engine = create_engine(DATABASE_URL)

# create a session factory ---> means you will use sessionlocal whenever you want to talk to database .
# bind = engine ---> tell sessionmaker which database coonection it should use.
# autocommit --> not to automatically commit changes to database after each operation
# autoflush --> not automatically flush changes to databse befor a query is run.
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

# Declare a base class for models to inherit from
Base = declarative_base()
# this base class all your model call will inherits from and tells sqlalchemy "this is a model/table"


# get_db() is responsible for creating and closing a database session
def get_db():
    db: Session = SessionLocal() # create new session
    try:
        yield db # pass it to route
    finally:
        db.close() # close database after request end.