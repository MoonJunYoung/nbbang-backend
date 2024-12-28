from base.exceptions import PaymentInMemberDeleteExcption
from member.domain import Member


class Payment:
    def __init__(
        self, id, place, price, pay_member_id, attend_member_ids, meeting_id
    ) -> None:
        self.id = id
        self.place = place
        self.price = price
        self.pay_member_id = pay_member_id
        self.attend_member_ids = attend_member_ids
        self.meeting_id = meeting_id

    def check_in_member(self, member: Member):
        for attend_member_id in self.attend_member_ids:
            if member.id == attend_member_id:
                raise PaymentInMemberDeleteExcption

    def set_split_price(self):
        attend_members_count = len(self.attend_member_ids)
        if not self.attend_member_ids:
            return 0
        split_price = (
            self.price // attend_members_count + 1
            if self.price % attend_members_count
            else self.price / attend_members_count
        )
        self.split_price = split_price

    def set_attend_members_name(self, members: list[Member]):
        self.attend_member = list()
        for member in members:
            for attend_member_id in self.attend_member_ids:
                if member.id == attend_member_id:
                    self.attend_member.append(member.name)

    def set_pay_member_name(self, members: list[Member]):
        for member in members:
            if member.id == self.pay_member_id:
                self.pay_member = member.name
