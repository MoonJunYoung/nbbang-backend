from typing import Optional

from base.database_connector import get_db_session
from base.exceptions import catch_exception
from base.token import Token
from fastapi import APIRouter, Depends, Header, Request, Response
from meeting.service import MeetingService
from pydantic import BaseModel

meeting_service = MeetingService()


class MeetingData(BaseModel):
    name: str = None
    date: str = None


class DepositInformationData(BaseModel):
    bank: Optional[str] = None
    account_number: Optional[str] = None
    kakao_deposit_id: Optional[str] = None


class MeetingPresentation:
    router = APIRouter(prefix="/api/meeting")

    @router.post("", status_code=201)
    async def add(
        request: Request,
        response: Response,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = await meeting_service.add(user_id, db_session)

            response.headers["Location"] = f"meeting/{meeting.id}"
        except Exception as e:
            catch_exception(e, request)

    @router.get("", status_code=200)
    async def read_meetings(
        Authorization=Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meetings = await meeting_service.read_meetings(user_id, db_session)
            return meetings
        except Exception as e:
            catch_exception(e)

    @router.get("/share-page", status_code=200)
    async def read_share_page(uuid: str, db_session=Depends(get_db_session)):
        try:
            share_page = await meeting_service.read_share_page(uuid, db_session)
            return share_page

        except Exception as e:
            catch_exception(e)

    @router.get("/{meeting_id}", status_code=200)
    async def read(
        meeting_id: int, Authorization=Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = await meeting_service.read(
                id=meeting_id, user_id=user_id, db_session=db_session
            )
            return meeting
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}", status_code=200)
    async def edit(
        meeting_id: int,
        meeting_data: MeetingData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await meeting_service.edit_information(
                id=meeting_id,
                name=meeting_data.name,
                date=meeting_data.date,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{meeting_id}", status_code=200)
    async def remove(
        meeting_id: int, Authorization=Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await meeting_service.remove(
                id=meeting_id, user_id=user_id, db_session=db_session
            )
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}/kakao-deposit-id", status_code=200)
    async def edit_kakao_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await meeting_service.edit_kakao_deposit(
                id=meeting_id,
                user_id=user_id,
                kakao_deposit_id=deposit_information_data.kakao_deposit_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}/bank-account", status_code=200)
    async def edit_toss_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await meeting_service.edit_toss_deposit(
                id=meeting_id,
                user_id=user_id,
                bank=deposit_information_data.bank,
                account_number=deposit_information_data.account_number,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)
