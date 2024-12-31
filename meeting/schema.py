from typing import Optional

from pydantic import BaseModel


class MeetingData(BaseModel):
    name: str = None
    date: str = None


class SimpleMeetingDataRequest(MeetingData):
    price: int = None
    member_count: int = None


class DepositInformationData(BaseModel):
    bank: Optional[str] = None
    account_number: Optional[str] = None
    kakao_deposit_id: Optional[str] = None
