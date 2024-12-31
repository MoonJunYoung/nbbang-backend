from typing import Optional

from fastapi import APIRouter, Depends, Header, Request, Response
from pydantic import BaseModel

from base.database_connector import get_db_session
from base.exceptions import catch_exception
from base.token import Token
from meeting.schema import DepositInformationData, MeetingData, SimpleMeetingDataRequest
from meeting.service import MeetingService

meeting_service = MeetingService()


class MeetingPresentation:
    router = APIRouter(prefix="/meeting")

    @router.post("", status_code=201)
    def create_meeting(
        request: Request,
        response: Response,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.add(user_id, db_session)

            response.headers["Location"] = f"meeting/{meeting.id}"
        except Exception as e:
            catch_exception(e, request)

    @router.post("/simple", status_code=201)
    def create_simple_meeting(
        request: Request,
        response: Response,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.create_simple_meeting(user_id, db_session)

            response.headers["Location"] = f"meeting/{meeting.id}"
        except Exception as e:
            catch_exception(e, request)

    @router.get("/simple/{meeting_id}", status_code=200)
    def read_simple_meeting(
        request: Request,
        meeting_id: int,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.read_simple_meeting(meeting_id, user_id, db_session)
            return meeting
        except Exception as e:
            catch_exception(e, request)

    @router.patch("/simple/{meeting_id}", status_code=200)
    def update_simple_meeting_data(
        request: Request,
        meeting_id: int,
        simple_meeting_data_request: SimpleMeetingDataRequest,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.update_simple_meeting_data(meeting_id, user_id, simple_meeting_data_request, db_session)
        except Exception as e:
            catch_exception(e, request)

    @router.get("", status_code=200)
    def read_meetings(Authorization=Depends(Token.get_token_by_authorization), db_session=Depends(get_db_session)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meetings = meeting_service.read_meetings(user_id, db_session)
            return meetings
        except Exception as e:
            catch_exception(e)

    @router.get("/share-page", status_code=200)
    def read_share_page(uuid: str, db_session=Depends(get_db_session)):
        try:
            share_page = meeting_service.read_share_page(uuid, db_session)
            return share_page

        except Exception as e:
            catch_exception(e)

    @router.get("/{meeting_id}", status_code=200)
    def read(meeting_id: int, Authorization=Depends(Token.get_token_by_authorization), db_session=Depends(get_db_session)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting = meeting_service.read(id=meeting_id, user_id=user_id, db_session=db_session)
            return meeting
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}", status_code=200)
    def edit(
        meeting_id: int,
        meeting_data: MeetingData,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit_information(
                id=meeting_id,
                name=meeting_data.name,
                date=meeting_data.date,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{meeting_id}", status_code=200)
    def remove(meeting_id: int, Authorization=Depends(Token.get_token_by_authorization), db_session=Depends(get_db_session)):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.remove(id=meeting_id, user_id=user_id, db_session=db_session)
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}/kakao-deposit-id", status_code=200)
    def edit_kakao_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit_kakao_deposit(
                id=meeting_id,
                user_id=user_id,
                kakao_deposit_id=deposit_information_data.kakao_deposit_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.put("/{meeting_id}/bank-account", status_code=200)
    def edit_toss_deposit_information(
        meeting_id: int,
        deposit_information_data: DepositInformationData,
        Authorization=Depends(Token.get_token_by_authorization),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            meeting_service.edit_toss_deposit(
                id=meeting_id,
                user_id=user_id,
                bank=deposit_information_data.bank,
                account_number=deposit_information_data.account_number,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)
