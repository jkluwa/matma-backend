from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgres://zcblmxmoizaiza:b89b67c4fe5586a77cfd22e0e1b3712d1c8cbba2ebb2786be0789c3c81843c0e@ec2-176-34-222-188.eu-west-1.compute.amazonaws.com:5432/dc7qdb3s7pg790"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
