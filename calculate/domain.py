from member.domain import Member
from payment.domain import Payment


class Calculate:
    def __init__(self, members: list[Member], payments: list[Payment]) -> None:
        self.members = members
        self.payments = payments

    def split_payments(self):
        for payment in self.payments:
            payment.set_split_price()
            payment.set_attend_members_name(self.members)
            payment.set_pay_member_name(self.members)

    def split_members(self):
        for payment in self.payments:
            payment.set_split_price()
            self._reduce_pay_member_amount(payment)
            self._add_attend_member_amount(payment)

    def _reduce_pay_member_amount(self, payment: Payment):
        for member in self.members:
            if member.id == payment.pay_member_id:
                member.add_amount(-payment.price)

    def _add_attend_member_amount(self, payment: Payment):
        for member in self.members:
            for member_id in payment.attend_member_ids:
                if member_id == member.id:
                    member.add_amount(payment.split_price)
