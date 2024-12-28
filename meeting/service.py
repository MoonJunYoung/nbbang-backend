from base.exceptions import IncompleteShareExcption, SharePageNotMeetingExcption
from calculate.domain import Calculate
from meeting.domain import Meeting
from meeting.repository import MeetingRepository
from member.domain import Member
from member.repository import MemberRepository
from payment.domain import Payment
from payment.repository import PaymentRepository
from user.domain import User
from user.repository import UserRepository


class MeetingService:
    def __init__(self) -> None:
        self.meeting_repository = MeetingRepository()
        self.member_repository = MemberRepository()
        self.payment_repository = PaymentRepository()
        self.user_repository = UserRepository()

    async def add(self, user_id, db_session):
        user = await self.user_repository.read_by_user_id(user_id, db_session)
        meeting = Meeting.create_template(user_id)
        meeting.load_user_deposit_information(user)
        await self.meeting_repository.create(meeting, db_session)
        return meeting

    async def edit_information(self, id, user_id, name, date, db_session):
        meeting = await self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_information(name, date)
        await self.meeting_repository.update_information(meeting, db_session)

    async def edit_kakao_deposit(self, id, user_id, kakao_deposit_id, db_session):
        meeting = await self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_kakao_deposit_information(kakao_deposit_id)
        await self.meeting_repository.update_kakao_deposit(meeting, db_session)

    async def edit_toss_deposit(self, id, user_id, bank, account_number, db_session):
        meeting = await self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_toss_deposit_information(bank, account_number)
        await self.meeting_repository.update_toss_deposit(meeting, db_session)

    async def remove(self, id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        await self.meeting_repository.delete(meeting, db_session)
        await self.member_repository.delete_by_meeting_id(meeting.id, db_session)
        await self.payment_repository.delete_by_meeting_id(meeting.id, db_session)

    async def read(self, id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    async def read_meetings(self, user_id, db_session):
        meetings = await self.meeting_repository.read_list_by_user_id(
            user_id, db_session
        )
        return meetings

    async def read_share_page(self, uuid, db_session):
        meeting = await self.meeting_repository.read_by_uuid(uuid, db_session)
        if not meeting:
            raise SharePageNotMeetingExcption
        members = await self.member_repository.read_list_by_meeting_id(
            meeting.id, db_session
        )
        payments = await self.payment_repository.read_list_by_meeting_id(
            meeting.id, db_session
        )
        if not members or not payments:
            raise IncompleteShareExcption

        calculate = Calculate(members=members, payments=payments)
        calculate.split_payments()
        calculate.split_members()

        for member in members:
            member.create_deposit_link(meeting)
        return {"meeting": meeting, "members": members, "payments": payments}
