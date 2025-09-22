import json
from typing import Optional

from fastapi import APIRouter, Depends, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from base.exceptions import NotAgerrmentExcption, catch_exception
from base.security import Token
from user.service import UserService, get_user_service


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


def oauth_login(
    platform,
    oauth: OauthData,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    if platform == "kakao":
        get_user_platform_information = Token.get_user_name_and_platform_id_by_kakao_oauth
    elif platform == "naver":
        get_user_platform_information = Token.get_user_name_and_platform_id_by_naver_oauth
    elif platform == "google":
        get_user_platform_information = Token.get_user_name_and_platform_id_by_google_oauth

    if oauth.token:
        name, platform_id = get_user_platform_information(oauth.token)
        user = user_service.oauth_signin(name, platform_id, platform)
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
        user = user_service.oauth_signup(oauth.name, oauth.platform_id, oauth.platform)
        return Token.create_token_by_user_id(user.id)
    else:
        raise NotAgerrmentExcption


class UserPresentation:
    router = APIRouter(prefix="/user")

    @router.get("", status_code=200)
    def read(
        Authorization: str = Depends(Token.get_token_by_authorization),
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(Authorization)
            return user_service.read(user_id)

        except Exception as e:
            catch_exception(e)

    @router.delete("", status_code=204)
    def delete(
        Authorization: str = Depends(Token.get_token_by_authorization),
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(Authorization)
            user_service.delete(user_id)

        except Exception as e:
            catch_exception(e)

    @router.post("/sign-up", status_code=201)
    def sign_up(
        login_data: LogInData,
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = user_service.sign_up(
                identifier=login_data.identifier,
                password=login_data.password,
                name=login_data.name,
            )
            return Token.create_token_by_user_id(user_id)

        except Exception as e:
            catch_exception(e)

    @router.post("/sign-in", status_code=201)
    def sign_in(
        login_data: LogInData,
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = user_service.sign_in(
                identifier=login_data.identifier,
                password=login_data.password,
            )
            return Token.create_token_by_user_id(user_id)
        except Exception as e:
            catch_exception(e)

    @router.post("/google-login", status_code=201)
    def google_login(
        oauth: OauthData,
        request: Request,
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            platform = "google"
            return oauth_login(platform, oauth, request, user_service)

        except Exception as e:
            catch_exception(e)

    @router.post("/kakao-login", status_code=201)
    def kakao_login(
        oauth: OauthData,
        request: Request,
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            platform = "kakao"
            return oauth_login(platform, oauth, request, user_service)
        except Exception as e:
            catch_exception(e)

    @router.post("/naver-login", status_code=201)
    def naver_login(
        oauth: OauthData,
        request: Request,
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            platform = "naver"
            return oauth_login(platform, oauth, request, user_service)
        except Exception as e:
            catch_exception(e)

    @router.put("/kakao-deposit-id", status_code=200)
    def edit_kakao_deposit_information(
        deposit_information_data: DepositInformationData,
        Authorization=Depends(Token.get_token_by_authorization),
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            user_service.edit_kakao_deposit(
                user_id=user_id,
                kakao_deposit_id=deposit_information_data.kakao_deposit_id,
            )
        except Exception as e:
            catch_exception(e)

    @router.put("/bank-account", status_code=200)
    def edit_toss_deposit_information(
        deposit_information_data: DepositInformationData,
        Authorization=Depends(Token.get_token_by_authorization),
        user_service: UserService = Depends(get_user_service),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            user_service.edit_toss_deposit(
                user_id=user_id,
                bank=deposit_information_data.bank,
                account_number=deposit_information_data.account_number,
            )
        except Exception as e:
            catch_exception(e)
