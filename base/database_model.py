import os

from dotenv import load_dotenv
from sqlalchemy import JSON, Boolean, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base

from base.database_connector import engine

load_dotenv()
Base = declarative_base()


class UserModel(Base):
    __tablename__ = "user"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    platform = Column(String)
    platform_id = Column(String)
    account_number = Column(LargeBinary)
    bank = Column(LargeBinary)
    kakao_deposit_id = Column(String)
    identifier = Column(String)
    password = Column(String)

    def __init__(
        self,
        id,
        name,
        platform_id,
        platform,
        bank,
        account_number,
        kakao_deposit_id,
        identifier,
        password,
    ):
        self.id = id
        self.name = name
        self.platform_id = platform_id
        self.platform = platform
        self.account_number = account_number
        self.bank = bank
        self.kakao_deposit_id = kakao_deposit_id
        self.identifier = identifier
        self.password = password


class MeetingModel(Base):
    __tablename__ = "meeting"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    user_id = Column(Integer)
    uuid = Column(String)
    account_number = Column(LargeBinary)
    bank = Column(LargeBinary)
    kakao_deposit_id = Column(String)
    is_simple = Column(Boolean)
    simple_price = Column(Integer)
    simple_member_count = Column(Integer)
    images = Column(JSON)

    def __init__(self, id, name, date, user_id, uuid, account_number, bank, kakao_deposit_id, is_simple, simple_price, simple_member_count, images):
        self.id = id
        self.name = name
        self.date = date
        self.user_id = user_id
        self.uuid = uuid
        self.account_number = account_number
        self.bank = bank
        self.kakao_deposit_id = kakao_deposit_id
        self.is_simple = is_simple
        self.simple_price = simple_price
        self.simple_member_count = simple_member_count
        self.images = images


class MemberModel(Base):
    __tablename__ = "member"
    id = Column("id", Integer, primary_key=True)
    name = Column(String)
    leader = Column(Boolean)
    meeting_id = Column(Integer)

    def __init__(self, id, name, leader, meeting_id):
        self.id = id
        self.name = name
        self.leader = leader
        self.meeting_id = meeting_id


class PaymentModel(Base):
    __tablename__ = "payment"
    id = Column("id", Integer, primary_key=True)
    place = Column(String)
    price = Column(Integer)
    pay_member_id = Column(Integer)
    attend_member_ids = Column(String)
    meeting_id = Column(Integer)
    order_no = Column(Integer, default=None, nullable=True)

    def __init__(self, id, place, price, pay_member_id, attend_member_ids, meeting_id, order_no=None):
        self.id = id
        self.place = place
        self.price = price
        self.pay_member_id = pay_member_id
        self.attend_member_ids = attend_member_ids
        self.meeting_id = meeting_id
        self.order_no = order_no


service_env = os.environ.get("SERVICE_ENV")
if service_env == "dev":
    Base.metadata.create_all(engine)
