from base.database_connector import get_db_session
from base.exceptions import catch_exception
from base.token import Token
from fastapi import APIRouter, Depends, Header
from member.service import MemberService
from pydantic import BaseModel

member_service = MemberService()


class MemberData(BaseModel):
    name: str
    leader: bool


class MemberPresentation:
    router = APIRouter(prefix="/api/meeting/{meeting_id}/member")

    @router.post("", status_code=201)
    async def create(
        meeting_id,
        member_data: MemberData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await member_service.create(
                name=member_data.name,
                leader=member_data.leader,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.get("", status_code=200)
    async def read(
        meeting_id, Authorization=Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            members = await member_service.read(
                meeting_id, user_id=user_id, db_session=db_session
            )
            return members
        except Exception as e:
            catch_exception(e)

    @router.put("/{member_id}", status_code=200)
    async def update(
        meeting_id: int,
        member_id: int,
        member_data: MemberData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await member_service.update(
                id=member_id,
                name=member_data.name,
                leader=member_data.leader,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{member_id}", status_code=200)
    async def delete(
        meeting_id: int,
        member_id: int,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await member_service.delete(
                member_id=member_id,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)
