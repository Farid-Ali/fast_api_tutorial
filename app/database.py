from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/<hostname>:<port-number>/<database-name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/fastAPI_tutorial'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
#For use row SQL using psycopg2
        
# while True:
#     try:
#         connection = psycopg2.connect(
#             host='localhost', 
#             database='fastAPI_tutorial', 
#             user='postgres', 
#             password='postgres',
#             cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Successfully connected to Database:)")
#         break
#     except Exception as error:
#         print("Database connection failed:(")
#         print("Error: ", error)
#         time.sleep(2)