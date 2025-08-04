from fastapi import APIRouter, Depends
from pydantic import BaseModel

from base.exceptions import catch_exception
from base.security import Token
from member.service import MemberService, get_member_service


class MemberData(BaseModel):
    name: str
    leader: bool


class MemberPresentation:
    router = APIRouter(prefix="/meeting/{meeting_id}/member")

    @router.post("", status_code=201)
    def create(
        meeting_id,
        member_data: MemberData,
        Authorization=Depends(Token.get_token_by_authorization),
        member_service: MemberService = Depends(get_member_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            member_service.create(
                name=member_data.name,
                leader=member_data.leader,
                meeting_id=meeting_id,
                user_id=user_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.get("", status_code=200)
    def read(
        meeting_id,
        Authorization=Depends(Token.get_token_by_authorization),
        member_service: MemberService = Depends(get_member_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            members = member_service.read(meeting_id, user_id=user_id)
            return members
        except Exception as e:
            catch_exception(e)

    @router.put("/{member_id}", status_code=200)
    def update(
        meeting_id: int,
        member_id: int,
        member_data: MemberData,
        Authorization=Depends(Token.get_token_by_authorization),
        member_service: MemberService = Depends(get_member_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            member_service.update(
                id=member_id,
                name=member_data.name,
                leader=member_data.leader,
                meeting_id=meeting_id,
                user_id=user_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{member_id}", status_code=200)
    def delete(
        meeting_id: int,
        member_id: int,
        Authorization=Depends(Token.get_token_by_authorization),
        member_service: MemberService = Depends(get_member_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            member_service.delete(
                member_id=member_id,
                meeting_id=meeting_id,
                user_id=user_id,
            )
        except Exception as e:
            catch_exception(e)
