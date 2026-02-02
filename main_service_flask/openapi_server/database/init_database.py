from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from dotenv import load_dotenv
load_dotenv()

try:
    USER_NAME = os.getenv("USER_NAME")
    USER_PASSWORD = os.getenv("USER_PASSWORD")
    DB_URL = os.getenv("DB_URL")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    if not USER_NAME or not USER_PASSWORD or not DB_URL or not DB_NAME or not DB_PORT: raise TypeError
except Exception as e:
    #TO DO stop the server startup process, as it was unable to connect to database due to lack of parameters 
    print(e)

DATABASE_URL = "postgresql://" + USER_NAME + ':' + USER_PASSWORD + '@' + DB_URL + ':' + DB_PORT + '/' + DB_NAME

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

def init_schema():
    from openapi_server.database.tables import CandidateDB, InternshipDB
    Base.metadata.create_all(bind=engine)
