from meeting.repository import MeetingRepository
from meeting.service import MeetingService
from user.domain import User
from user.exceptions import IdentifierNotFoundException
from user.repository import UserRepository


class UserService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.meeting_repository = MeetingRepository()
        self.meeting_service = MeetingService()

    async def sign_up(self, identifier, password, name, db_session):
        user = User(
            id=None,
            name=name,
            identifier=identifier,
            password=password,
        )
        if await self.user_repository.read_by_identifier(
            identifier=user.identifier, db_session=db_session
        ):
            user.identifier_is_not_unique()
        user.password_encryption()
        await self.user_repository.create(user, db_session=db_session)
        return user.id

    async def sign_in(self, identifier, password, db_session):
        user = await self.user_repository.read_by_identifier(
            identifier, db_session=db_session
        )
        if not user:
            raise IdentifierNotFoundException(identifier=identifier)
        user.check_password_match(password)
        return user.id

    async def oauth_signin(self, name, platform_id, platform, db_session):
        user = User(
            id=None,
            name=name,
            platform_id=platform_id,
            platform=platform,
            identifier=None,
            password=None,
        )
        existing_user = await self.user_repository.read_by_platform_id(
            platform_id=user.platform_id,
            platform=user.platform,
            db_session=db_session,
        )
        if not existing_user:
            return None
        return existing_user

    async def oauth_signup(self, name, platform_id, platform, db_session):
        user = User(
            id=None,
            name=name,
            platform_id=platform_id,
            platform=platform,
            identifier=None,
            password=None,
        )
        await self.user_repository.create(user, db_session=db_session)
        return user

    async def read(self, user_id, db_session):
        user = await self.user_repository.read_by_user_id(
            user_id, db_session=db_session
        )
        del user.password
        return user

    async def edit_kakao_deposit(self, user_id, kakao_deposit_id, db_session):
        user = await self.user_repository.read_by_user_id(
            user_id, db_session=db_session
        )
        user.update_kakao_deposit_information(kakao_deposit_id)
        await self.user_repository.update_kakao_deposit(user, db_session=db_session)

    async def edit_toss_deposit(self, user_id, bank, account_number, db_session):
        user = await self.user_repository.read_by_user_id(
            user_id, db_session=db_session
        )
        user.update_toss_deposit_information(bank, account_number)
        await self.user_repository.update_toss_deposit(user, db_session=db_session)

    async def delete(self, user_id, db_session):
        user = await self.user_repository.read_by_user_id(
            user_id, db_session=db_session
        )
        meetings = await self.meeting_repository.read_list_by_user_id(
            user.id, db_session
        )
        for meeting in meetings:
            await self.meeting_service.remove(meeting.id, user.id, db_session)
        await self.user_repository.delete(user.id, db_session)
