from base.dto import PaymentDTO, set_DTO
from calculate.domain import Calculate
from meeting.domain import Meeting
from meeting.repository import MeetingRepository
from member.domain import Member
from member.repository import MemberRepository
from payment.domain import Payment
from payment.repository import PaymentRepository


class PaymentService:
    def __init__(self) -> None:
        self.meeting_repository = MeetingRepository()
        self.payment_repository = PaymentRepository()
        self.memeber_repository = MemberRepository()

    async def create(
        self,
        place,
        price,
        pay_member_id,
        attend_member_ids,
        meeting_id,
        user_id,
        db_session,
    ):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=None,
            place=place,
            price=price,
            pay_member_id=pay_member_id,
            attend_member_ids=attend_member_ids,
            meeting_id=meeting_id,
        )
        await self.payment_repository.create(payment, db_session)
        return payment

    async def update(
        self,
        id,
        place,
        price,
        pay_member_id,
        attend_member_ids,
        meeting_id,
        user_id,
        db_session,
    ):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=id,
            place=place,
            price=price,
            pay_member_id=pay_member_id,
            attend_member_ids=attend_member_ids,
            meeting_id=meeting_id,
        )
        await self.payment_repository.update(payment, db_session)

    async def delete(self, id, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        payment = Payment(
            id=id,
            place=None,
            price=None,
            pay_member_id=None,
            attend_member_ids=None,
            meeting_id=meeting_id,
        )
        await self.payment_repository.delete(payment, db_session)

    async def read(self, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        payments = await self.payment_repository.read_list_by_meeting_id(
            meeting.id, db_session
        )
        members = await self.memeber_repository.read_list_by_meeting_id(
            meeting.id, db_session
        )
        calculate = Calculate(members=members, payments=payments)
        calculate.split_payments()

        return set_DTO(PaymentDTO, payments)
