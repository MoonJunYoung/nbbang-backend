from member.domain import Member
from payment.domain import Payment


def set_DTO(DTO, domains):
    if hasattr(domains, "__iter__"):
        result = list()
        for domain in domains:
            result.append(DTO(domain))
    else:
        result = DTO(domains)
    return result


class MemberDTO:
    def __init__(self, member: Member) -> None:
        self.id = member.id
        self.name = member.name
        self.leader = member.leader
        self.amount = member.amount
        self.tipped_amount = member.tipped_amount


class PaymentDTO:
    def __init__(self, payment: Payment) -> None:
        self.id = payment.id
        self.place = payment.place
        self.price = payment.price
        self.split_price = payment.split_price
        self.pay_member = payment.pay_member
        self.attend_member = payment.attend_member
        self.attend_member_ids = payment.attend_member_ids
