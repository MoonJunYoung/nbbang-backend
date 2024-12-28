import json
from typing import Optional

from base.database_connector import get_db_session
from base.exceptions import NotAgerrmentExcption, catch_exception
from base.token import Token
from fastapi import APIRouter, Depends, Header, Response, status, Request
from pydantic import BaseModel
from user.service import UserService

user_service = UserService()


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


async def oauth_login(platform, oauth: OauthData, request: Request, db_session):
    if platform == "kakao":
        get_user_platform_information = (
            Token.get_user_name_and_platform_id_by_kakao_oauth
        )
    elif platform == "naver":
        get_user_platform_information = (
            Token.get_user_name_and_platform_id_by_naver_oauth
        )
    elif platform == "google":
        get_user_platform_information = (
            Token.get_user_name_and_platform_id_by_google_oauth
        )

    if oauth.token:
        name, platform_id = await get_user_platform_information(oauth.token)
        user = await user_service.oauth_signin(name, platform_id, platform, db_session)
        if not user:
            return Response(
                content=json.dumps(
                    {
                        "platform": platform,
                        "platform_id": platform_id,
                        "name": name,
                        "agreement": False,
                    }
                ),
                status_code=status.HTTP_202_ACCEPTED,
                headers={"Location": str(request.url)},
            )
        return Token.create_token_by_user_id(user.id)

    elif oauth.agreement and oauth.platform and oauth.platform_id and oauth.name:
        user = await user_service.oauth_signup(
            oauth.name, oauth.platform_id, oauth.platform, db_session
        )
        return Token.create_token_by_user_id(user.id)
    else:
        raise NotAgerrmentExcption


class UserPresentation:
    router = APIRouter(prefix="/api/user")

    @router.get("", status_code=200)
    async def read(
        Authorization: str = Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(Authorization)
            return await user_service.read(user_id, db_session)

        except Exception as e:
            catch_exception(e)

    @router.delete("", status_code=204)
    async def delete(
        Authorization: str = Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(Authorization)
            await user_service.delete(user_id, db_session)

        except Exception as e:
            catch_exception(e)

    @router.post("/sign-up", status_code=201)
    async def sign_up(login_data: LogInData, db_session=Depends(get_db_session)):
        try:
            user_id = await user_service.sign_up(
                identifier=login_data.identifier,
                password=login_data.password,
                name=login_data.name,
                db_session=db_session,
            )
            return Token.create_token_by_user_id(user_id)

        except Exception as e:
            catch_exception(e)

    @router.post("/sign-in", status_code=201)
    async def sign_in(login_data: LogInData, db_session=Depends(get_db_session)):
        try:
            user_id = await user_service.sign_in(
                identifier=login_data.identifier,
                password=login_data.password,
                db_session=db_session,
            )
            return Token.create_token_by_user_id(user_id)
        except Exception as e:
            catch_exception(e)

    @router.post("/google-login", status_code=201)
    async def google_login(
        oauth: OauthData,
        request: Request,
        db_session=Depends(get_db_session),
    ):
        try:
            platform = "google"
            return await oauth_login(platform, oauth, request, db_session)

        except Exception as e:
            catch_exception(e)

    @router.post("/kakao-login", status_code=201)
    async def kakao_login(
        oauth: OauthData,
        request: Request,
        db_session=Depends(get_db_session),
    ):
        try:
            platform = "kakao"
            return await oauth_login(platform, oauth, request, db_session)
        except Exception as e:
            catch_exception(e)

    @router.post("/naver-login", status_code=201)
    async def naver_login(
        oauth: OauthData,
        request: Request,
        db_session=Depends(get_db_session),
    ):
        try:
            platform = "naver"
            return await oauth_login(platform, oauth, request, db_session)
        except Exception as e:
            catch_exception(e)

    @router.put("/kakao-deposit-id", status_code=200)
    async def edit_kakao_deposit_information(
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await user_service.edit_kakao_deposit(
                user_id=user_id,
                kakao_deposit_id=deposit_information_data.kakao_deposit_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.put("/bank-account", status_code=200)
    async def edit_toss_deposit_information(
        deposit_information_data: DepositInformationData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await user_service.edit_toss_deposit(
                user_id=user_id,
                bank=deposit_information_data.bank,
                account_number=deposit_information_data.account_number,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)
