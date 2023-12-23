from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# SQLALCHEMY_DATABASE_URL = 'postgresssql://<username>:<password>@<ip address/hostname>/<database_name>';
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}';

engine = create_engine(SQLALCHEMY_DATABASE_URL);

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

Base = declarative_base()

# Dependency
def get_db() :
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# We are using pydantic directly this is a raw method of connecting to database
# while True:
#     try:
#         conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', password='Sandeepsunil@23', cursor_factory=RealDictCursor)    
#         cursor = conn.cursor()
#         print("Database Connection was successful")
#         break
#     except Exception as e:
#         print('Connection to Database Failed')
#         print('Error :-- ', e)
#         time.sleep(5)