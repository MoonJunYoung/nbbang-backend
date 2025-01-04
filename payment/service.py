from fastapi import Depends
from requests import Session

from base.database_connector import get_db_session
from base.dto import PaymentDTO, set_DTO
from calculate.domain import Calculate
from meeting.repository import MeetingRepository
from member.repository import MemberRepository
from payment.domain import Payment
from payment.repository import PaymentRepository


def get_payment_service(db_session: Session = Depends(get_db_session)):
    return PaymentService(db_session=db_session)


class PaymentService:
    def __init__(self, db_session: Session) -> None:
        self.meeting_repository = MeetingRepository(db_session)
        self.payment_repository = PaymentRepository(db_session)
        self.memeber_repository = MemberRepository(db_session)

    def create(
        self,
        place,
        price,
        pay_member_id,
        attend_member_ids,
        meeting_id,
        user_id,
    ):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=None,
            place=place,
            price=price,
            pay_member_id=pay_member_id,
            attend_member_ids=attend_member_ids,
            meeting_id=meeting_id,
        )
        self.payment_repository.create(payment)
        return payment

    def update(
        self,
        id,
        place,
        price,
        pay_member_id,
        attend_member_ids,
        meeting_id,
        user_id,
    ):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=id,
            place=place,
            price=price,
            pay_member_id=pay_member_id,
            attend_member_ids=attend_member_ids,
            meeting_id=meeting_id,
        )
        self.payment_repository.update(payment)

    def delete(self, id, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=id,
            place=None,
            price=None,
            pay_member_id=None,
            attend_member_ids=None,
            meeting_id=meeting_id,
        )
        self.payment_repository.delete(payment)

    def read(self, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        payments = self.payment_repository.read_list_by_meeting_id(meeting.id)
        members = self.memeber_repository.read_list_by_meeting_id(meeting.id)
        calculate = Calculate(members=members, payments=payments)
        calculate.split_payments()

        return set_DTO(PaymentDTO, payments)

    def update_payment_order(self, meeting_id, payment_order_data, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        self.payment_repository.update_order(payment_order_data)
