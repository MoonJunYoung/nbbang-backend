import datetime
import math
import re
import uuid
from urllib import parse

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
        is_simple=False,
        simple_price=None,
        simple_member_count=None,
        simple_member_amount=None,
        images=[],
    ) -> None:
        self.id = id
        self.name = name
        self.date = Date(date).date
        self.user_id = user_id
        self.uuid = uuid
        self.toss_deposit_information = TossDepositInformation(bank, account_number)
        self.kakao_deposit_information = KakaoDepositInformation(kakao_deposit_id)
        self.is_simple = is_simple
        self.simple_price = simple_price
        self.simple_member_count = simple_member_count
        self.simple_member_amount = simple_member_amount
        self.images = images
        if self.is_simple and self.simple_price and self.simple_member_count:
            split_price = (
                self.simple_price // self.simple_member_count + 1
                if self.simple_price % self.simple_member_count
                else self.simple_price / self.simple_member_count
            )
            self.simple_member_amount = split_price

    @staticmethod
    def create_template(user_id):
        return Meeting(
            id=None,
            name="모임명을 설정해주세요",
            date=datetime.date.isoformat(datetime.date.today()),
            user_id=user_id,
            uuid=str(uuid.uuid4()),
        )

    @staticmethod
    def create_simple_template(user_id):
        return Meeting(
            id=None,
            name="모임명을 설정해주세요",
            date=datetime.date.isoformat(datetime.date.today()),
            user_id=user_id,
            uuid=str(uuid.uuid4()),
            is_simple=True,
            simple_price=None,
            simple_member_count=None,
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
        if self.is_simple:
            self.share_link = f"https://nbbang.shop/share?simple-meeting={self.uuid}"
        else:
            self.share_link = f"https://nbbang.shop/share?meeting={self.uuid}"

    def _create_toss_deposit_link(self, amount, bank, account_number):
        base_url = "supertoss://send"
        params = {
            "amount": int(amount),
            "bank": bank,
            "accountNo": account_number,
        }
        encoded_params = parse.urlencode(params)
        encoded_url = f"{base_url}?{encoded_params}"
        return encoded_url

    def _create_kakako_deposit_link(self, amount, kakao_deposit_id):
        def _to_hex_value(value):
            return format(value * 524288, "x")

        base_url = "https://qr.kakaopay.com/{kakao_deposit_id}{hex_amount}"
        hex_amount = _to_hex_value(int(amount))
        send_link = base_url.format(
            kakao_deposit_id=kakao_deposit_id,
            hex_amount=hex_amount,
        )
        return send_link

    def _create_deposit_copy_text(self, amount, bank, account_number):
        return f"{bank} {account_number} {int(amount)}원"

    def create_simple_deposit_link(self):
        deposit_amount = self.simple_price // self.simple_member_count
        tipped_deposit_amount = math.ceil((self.simple_price / self.simple_member_count) / 10) * 10
        self.simple_tipped_member_amount = tipped_deposit_amount
        if self.toss_deposit_information.bank and self.toss_deposit_information.account_number:
            self.toss_deposit_link = self._create_toss_deposit_link(
                deposit_amount, self.toss_deposit_information.bank, self.toss_deposit_information.account_number
            )
            self.tipped_toss_deposit_link = self._create_toss_deposit_link(
                tipped_deposit_amount, self.toss_deposit_information.bank, self.toss_deposit_information.account_number
            )
            self.deposit_copy_text = self._create_deposit_copy_text(
                deposit_amount, self.toss_deposit_information.bank, self.toss_deposit_information.account_number
            )
            self.tipped_deposit_copy_text = self._create_deposit_copy_text(
                tipped_deposit_amount, self.toss_deposit_information.bank, self.toss_deposit_information.account_number
            )
        if self.kakao_deposit_information.kakao_deposit_id:
            self.kakao_deposit_link = self._create_kakako_deposit_link(deposit_amount, self.kakao_deposit_information.kakao_deposit_id)
            self.tipped_kakao_deposit_link = self._create_kakako_deposit_link(tipped_deposit_amount, self.kakao_deposit_information.kakao_deposit_id)


class Date:
    def __init__(self, date) -> None:
        self.date = date
        if self.date and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z$", self.date):
            dt = datetime.datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%fZ")
            self.date = dt.strftime("%Y-%m-%d")
