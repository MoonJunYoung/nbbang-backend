from typing import Optional

from pydantic import BaseModel


class MeetingRequest(BaseModel):
    name: str = None
    date: str = None


class SimpleMeetingRequest(MeetingRequest):
    simple_price: int = None
    simple_member_count: int = None


class DepositInformationRequest(BaseModel):
    bank: Optional[str] = None
    account_number: Optional[str] = None
    kakao_deposit_id: Optional[str] = None
