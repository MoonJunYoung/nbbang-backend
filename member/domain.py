import math
from urllib import parse

from base.exceptions import MemberIsLeaderDeleteExcption
from meeting.domain import Meeting


class Member:
    def __init__(
        self,
        id,
        name,
        leader,
        meeting_id,
        amount=0,
        tipped_amount=0,
        deposit_copy_data=None,
        tipped_deposit_copy_data=None,
    ) -> None:
        self.id = id
        self.name = name
        self.leader = leader
        self.meeting_id = meeting_id
        self.amount = amount
        self.tipped_amount = tipped_amount
        self.deposit_copy_data = deposit_copy_data
        self.tipped_deposit_copy_data = tipped_deposit_copy_data

    def delete_member_if_not_leader(self):
        if self.leader:
            raise MemberIsLeaderDeleteExcption

    def add_amount(self, amount):
        self.amount += amount
        self.tipped_amount = math.ceil(self.amount / 10) * 10

    def create_deposit_link(self, meeting: Meeting):
        if (
            meeting.toss_deposit_information.bank
            and meeting.toss_deposit_information.account_number
        ):
            self.toss_deposit_link = self._create_toss_deposit_link(
                self.amount,
                meeting.toss_deposit_information.bank,
                meeting.toss_deposit_information.account_number,
            )
            self.tipped_toss_deposit_link = self._create_toss_deposit_link(
                self.tipped_amount,
                meeting.toss_deposit_information.bank,
                meeting.toss_deposit_information.account_number,
            )
            self.deposit_copy_text = self._create_deposit_copy_text(
                self.amount,
                meeting.toss_deposit_information.bank,
                meeting.toss_deposit_information.account_number,
            )
            self.tipped_deposit_copy_text = self._create_deposit_copy_text(
                self.tipped_amount,
                meeting.toss_deposit_information.bank,
                meeting.toss_deposit_information.account_number,
            )
        if meeting.kakao_deposit_information.kakao_deposit_id:
            self.kakao_deposit_link = self._create_kakako_deposit_link(
                self.amount, meeting.kakao_deposit_information.kakao_deposit_id
            )
            self.tipped_kakao_deposit_link = self._create_kakako_deposit_link(
                self.tipped_amount, meeting.kakao_deposit_information.kakao_deposit_id
            )

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
