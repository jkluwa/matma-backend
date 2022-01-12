from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://doadmin:hQfmqZ1kA8PQfqvu@matma-do-user-10522895-0.b.db.ondigitalocean.com:25060/defaultdb"
ssl_args = {
    'ssl_ca': 'C:/Users/jkluw/Documents/matma rządzi/backend/ca-certificate.crt'}
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args=ssl_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
