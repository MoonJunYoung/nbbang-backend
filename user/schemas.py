from typing import Optional

from pydantic import BaseModel


class LogInData(BaseModel):
    identifier: str
    password: str
    name: str = None


class OauthData(BaseModel):
    token: str = None
    platform: str = None
    platform_id: str = None
    name: str = None
    agreement: bool = None


class DepositInformationData(BaseModel):
    bank: Optional[str] = None
    account_number: Optional[str] = None
    kakao_deposit_id: Optional[str] = None


class GuestUpdateData(BaseModel):
    longin_data: Optional[LogInData] = None
    oauth_data: Optional[OauthData] = None
