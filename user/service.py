from fastapi import Depends
from requests import Session

from base.database_connector import get_db_session
from meeting.repository import MeetingRepository
from meeting.service import MeetingService
from user.domain import User
from user.exceptions import IdentifierNotFoundException
from user.repository import UserRepository


def get_user_service(db_session: Session = Depends(get_db_session)):
    return UserService(db_session=db_session)


class UserService:
    def __init__(self, db_session: Session) -> None:
        self.user_repository = UserRepository(db_session)
        self.meeting_repository = MeetingRepository(db_session)
        self.meeting_service = MeetingService(db_session)

    def sign_up(self, identifier, password, name):
        user = User(
            id=None,
            name=name,
            identifier=identifier,
            password=password,
        )
        if self.user_repository.read_by_identifier(identifier=user.identifier):
            user.identifier_is_not_unique()
        user.password_encryption()
        self.user_repository.create(user)
        return user.id

    def sign_in(self, identifier, password):
        user = self.user_repository.read_by_identifier(identifier)
        if not user:
            raise IdentifierNotFoundException(identifier=identifier)
        user.check_password_match(password)
        return user.id

    def oauth_signin(self, name, platform_id, platform):
        user = User(
            id=None,
            name=name,
            platform_id=platform_id,
            platform=platform,
            identifier=None,
            password=None,
        )
        existing_user = self.user_repository.read_by_platform_id(
            platform_id=user.platform_id,
            platform=user.platform,
        )
        if not existing_user:
            return None
        return existing_user

    def oauth_signup(self, name, platform_id, platform):
        user = User(
            id=None,
            name=name,
            platform_id=platform_id,
            platform=platform,
            identifier=None,
            password=None,
        )
        self.user_repository.create(user)
        return user

    def read(self, user_id):
        user = self.user_repository.read_by_user_id(user_id)
        del user.password
        return user

    def edit_kakao_deposit(self, user_id, kakao_deposit_id):
        user = self.user_repository.read_by_user_id(user_id)
        user.update_kakao_deposit_information(kakao_deposit_id)
        self.user_repository.update_kakao_deposit(user)

    def edit_toss_deposit(self, user_id, bank, account_number):
        user = self.user_repository.read_by_user_id(user_id)
        user.update_toss_deposit_information(bank, account_number)
        self.user_repository.update_toss_deposit(user)

    def delete(self, user_id):
        user = self.user_repository.read_by_user_id(user_id)
        meetings = self.meeting_repository.read_list_by_user_id(user.id)
        for meeting in meetings:
            self.meeting_service.remove(meeting.id, user.id)
        self.user_repository.delete(user.id)
