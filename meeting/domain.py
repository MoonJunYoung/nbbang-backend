import datetime
import re
import uuid

from base.exceptions import MeetingUserMismatchException
from base.vo import KakaoDepositInformation, TossDepositInformation
from user.domain import User


class Meeting:
    def __init__(
        self,
        id,
        name,
        date,
        user_id,
        uuid=None,
        bank=None,
        account_number=None,
        kakao_deposit_id=None,
    ) -> None:
        self.id = id
        self.name = name
        self.date = Date(date).date
        self.user_id = user_id
        self.uuid = uuid
        self.toss_deposit_information = TossDepositInformation(bank, account_number)
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)

    @staticmethod
    def create_template(user_id):
        return Meeting(
            id=None,
            name="모임명을 설정해주세요",
            date=datetime.date.isoformat(datetime.date.today()),
            user_id=user_id,
            uuid=str(uuid.uuid4()),
        )

    def load_user_deposit_information(self, user: User):
        self.kakao_deposit_information = KakaoDepositInformation(user.kakao_deposit_information.kakao_deposit_id)
        self.toss_deposit_information = TossDepositInformation(
            user.toss_deposit_information.bank,
            user.toss_deposit_information.account_number,
        )

    def update_information(self, name, date):
        self.name = name
        self.date = Date(date).date

    def update_kakao_deposit_information(self, kakao_deposit_id):
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)

    def update_toss_deposit_information(self, bank, account_number):
        self.toss_deposit_information = TossDepositInformation(bank, account_number)

    def is_user_of_meeting(self, user_id):
        if not self.user_id == user_id:
            raise MeetingUserMismatchException(user_id, self.id)

    def create_share_link(self):
        self.share_link = f"https://nbbang.life/share?meeting={self.uuid}"


class Date:
    def __init__(self, date) -> None:
        self.date = date
        if self.date and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$", self.date):
            dt = datetime.datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.date = dt.strftime("%Y-%m-%d")
