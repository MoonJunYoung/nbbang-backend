from sqlalchemy.orm import Session

from base.database_model import UserModel
from user.domain import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User):
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
        self.db_session.add(user_model)
        self.db_session.commit()
        user.id = user_model.id

    def delete(self, user_id):
        user_model = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
        self.db_session.delete(user_model)
        self.db_session.commit()

    def read_by_identifier(self, identifier):
        user_model = self.db_session.query(UserModel).filter(UserModel.identifier == identifier).first()
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

    def read_by_platform_id(self, platform, platform_id):
        user_model = self.db_session.query(UserModel).filter(UserModel.platform == platform).filter(UserModel.platform_id == platform_id).first()
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

    def read_by_user_id(self, user_id):
        user_model = self.db_session.query(UserModel).filter(UserModel.id == user_id).first()
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

    def update_toss_deposit(self, user: User):
        user_model = self.db_session.query(UserModel).filter(UserModel.id == user.id).first()
        user_model.bank = user.toss_deposit_information.bank
        user_model.account_number = user.toss_deposit_information.account_number
        self.db_session.commit()

    def update_kakao_deposit(self, user: User):
        user_model = self.db_session.query(UserModel).filter(UserModel.id == user.id).first()
        user_model.kakao_deposit_id = user.kakao_deposit_information.kakao_deposit_id
        self.db_session.commit()
