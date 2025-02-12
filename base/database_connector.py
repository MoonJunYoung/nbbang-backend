import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

service_env = os.environ.get("SERVICE_ENV")

if service_env == "dev":
    engine = create_engine("mysql+pymysql://root:answnsdud1@localhost:3306/nbbang")
    SessionLocal = sessionmaker(bind=engine)

else:
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    user_name = os.environ.get("DB_USERNAME")
    passwd = os.environ.get("DB_PASSWD")
    database = os.environ.get("DB_DATABASE")
    if service_env == "test":
        engine = create_engine(f"mysql+pymysql://{user_name}:{passwd}@{host}:{port}/{database}-test")
    else:
        engine = create_engine(f"mysql+pymysql://{user_name}:{passwd}@{host}:{port}/{database}")
    SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MysqlCRUDTemplate:
    pass
