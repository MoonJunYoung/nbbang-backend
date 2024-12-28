from base.database_model import UserModel
from sqlalchemy.orm import Session
from user.domain import User


class UserRepository:
    async def create(self, user: User, db_session: Session):
        user_model = UserModel(
            id=None,
            name=user.name,
            platform_id=user.platform_id,
            platform=user.platform,
            account_number=None,
            bank=None,
            kakao_deposit_id=None,
            identifier=user.identifier,
            password=user.password,
        )
        db_session.add(user_model)
        db_session.commit()
        user.id = user_model.id

    async def delete(self, user_id, db_session: Session):
        user_model = db_session.query(UserModel).filter(UserModel.id == user_id).first()
        db_session.delete(user_model)
        db_session.commit()

    async def read_by_identifier(self, identifier, db_session: Session):
        user_model = (
            db_session.query(UserModel)
            .filter(UserModel.identifier == identifier)
            .first()
        )
        if not user_model:
            return None
        user = User(
            id=user_model.id,
            name=user_model.name,
            platform_id=user_model.platform_id,
            platform=user_model.platform,
            identifier=user_model.identifier,
            password=user_model.password,
        )
        return user

    async def read_by_platform_id(self, platform, platform_id, db_session: Session):
        user_model = (
            db_session.query(UserModel)
            .filter(UserModel.platform == platform)
            .filter(UserModel.platform_id == platform_id)
            .first()
        )
        if not user_model:
            return None
        user = User(
            id=user_model.id,
            name=user_model.name,
            platform_id=user_model.platform_id,
            platform=user_model.platform,
            identifier=user_model.identifier,
            password=user_model.password,
        )
        return user

    async def read_by_user_id(self, user_id, db_session: Session):
        user_model = db_session.query(UserModel).filter(UserModel.id == user_id).first()
        if not user_model:
            return None
        user = User(
            id=user_model.id,
            name=user_model.name,
            platform_id=user_model.platform_id,
            platform=user_model.platform,
            identifier=user_model.identifier,
            password=user_model.password,
            bank=user_model.bank,
            account_number=user_model.account_number,
            kakao_deposit_id=user_model.kakao_deposit_id,
        )
        return user

    async def update_toss_deposit(self, user: User, db_session: Session):
        user_model = db_session.query(UserModel).filter(UserModel.id == user.id).first()
        user_model.bank = user.toss_deposit_information.bank
        user_model.account_number = user.toss_deposit_information.account_number
        db_session.commit()

    async def update_kakao_deposit(self, user: User, db_session: Session):
        user_model = db_session.query(UserModel).filter(UserModel.id == user.id).first()
        user_model.kakao_deposit_id = user.kakao_deposit_information.kakao_deposit_id
        db_session.commit()
