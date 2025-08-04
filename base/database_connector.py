import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

service_env = os.environ.get("SERVICE_ENV")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user_name = os.environ.get("DB_USERNAME")
passwd = os.environ.get("DB_PASSWD")
database = os.environ.get("DB_DATABASE")
engine = create_engine(f"postgresql+psycopg2://{user_name}:{passwd}@{host}:{port}/postgres")
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MysqlCRUDTemplate:
    pass
