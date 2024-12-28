import datetime
import json
import os

import jwt
import requests
from base.exceptions import InvalidTokenException, MissingTokenException
from dotenv import load_dotenv

load_dotenv()
secret_key = os.environ.get("JWT_SECRET_KEY")
kakao_cilent_id = os.environ.get("KAKAO_CLIENT_ID")
kakao_redirect_url = os.environ.get("KAKAO_REDIRECT_URL")
naver_client_id = os.environ.get("NAVER_CLIENT_ID")
naver_client_secret = os.environ.get("NAVER_CLIENT_SECRET")
naver_state = os.environ.get("NAVER_STATE")


class Token:
    def create_token_by_user_id(user_id):
        payload = {
            "id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30),
        }
        token = jwt.encode(payload, secret_key)
        return token

    def get_user_id_by_token(token):
        if not token:
            raise MissingTokenException
        try:
            token_info = jwt.decode(token, secret_key, algorithms="HS256")
        except jwt.exceptions.DecodeError:
            raise InvalidTokenException
        token_user_id = token_info.get("id")
        return token_user_id

    async def get_user_name_and_platform_id_by_google_oauth(token):
        google_user_data = json.loads(
            requests.get(
                f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={token}"
            ).text
        )
        name = google_user_data.get("name")
        platform_id = str(google_user_data.get("id"))
        return name, platform_id

    async def get_user_name_and_platform_id_by_kakao_oauth(token):
        def _get_user_access_token_by_kakao_oauth(token):
            data = {
                "grant_type": "authorization_code",
                "client_id": kakao_cilent_id,
                "redirect_uri": kakao_redirect_url,
                "code": token,
            }
            kakao_token_data = json.loads(
                requests.post(
                    url=f"https://kauth.kakao.com/oauth/token", data=data
                ).text
            )
            access_token = kakao_token_data.get("access_token")
            return access_token

        access_token = _get_user_access_token_by_kakao_oauth(token)
        headers = {"Authorization": f"Bearer {access_token}"}
        kakao_user_data = json.loads(
            requests.get(url="https://kapi.kakao.com/v2/user/me", headers=headers).text
        )
        platform_id = str(kakao_user_data.get("id"))
        name = kakao_user_data.get("kakao_account").get("profile").get("nickname")
        return name, platform_id

    async def get_user_name_and_platform_id_by_naver_oauth(token):
        def _get_user_access_token_by_naver_oauth(token):
            naver_token_data = json.loads(
                requests.post(
                    url=f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={naver_client_id}&client_secret={naver_client_secret}&code={token}&state={naver_state}"
                ).text
            )
            access_token = naver_token_data.get("access_token")
            return access_token

        access_token = _get_user_access_token_by_naver_oauth(token)
        headers = {"Authorization": f"Bearer {access_token}"}
        naver_user_data = json.loads(
            requests.get(
                url="https://openapi.naver.com/v1/nid/me", headers=headers
            ).text
        )
        platform_id = str(naver_user_data.get("response").get("id"))
        name = naver_user_data.get("response").get("name")
        return name, platform_id
