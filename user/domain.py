import bcrypt
from base.vo import KakaoDepositInformation, TossDepositInformation
from user.exceptions import IdentifierAlreadyException, PasswordNotMatchException


class User:
    def __init__(
        self,
        id,
        name=None,
        platform_id=None,
        platform=None,
        identifier=None,
        password=None,
        bank=None,
        account_number=None,
        kakao_deposit_id=None,
    ) -> None:
        self.id = id
        self.name = name
        self.platform_id = platform_id
        self.platform = platform
        self.identifier = identifier
        self.password = password
        self.toss_deposit_information = TossDepositInformation(bank, account_number)
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)

    def identifier_is_not_unique(self):
        raise IdentifierAlreadyException(self.identifier)

    def password_encryption(self):
        salt = bcrypt.gensalt()
        encrypted = bcrypt.hashpw(self.password.encode("utf-8"), salt)
        self.password = encrypted.decode("utf-8")

    def check_password_match(self, password):
        if not bcrypt.checkpw(password.encode(), self.password.encode()):
            raise PasswordNotMatchException(
                identifier=self.identifier, password=password
            )

    def update_kakao_deposit_information(self, kakao_deposit_id):
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)

    def update_toss_deposit_information(self, bank, account_number):
        self.toss_deposit_information = TossDepositInformation(bank, account_number)
