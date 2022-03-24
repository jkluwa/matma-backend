from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib import parse

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:%s@localhost:3306/matma" % parse.quote_plus(
    "Sigma123@5")
ssl_args = {
    'ssl_ca': './ca-certificate.crt'}
engine = create_engine(SQLALCHEMY_DATABASE_URL,
                       connect_args=ssl_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
