from base.dto import MemberDTO, set_DTO
from base.exceptions import LeaderAlreadyException, MemberIsLeaderDeleteExcption
from calculate.domain import Calculate
from meeting.domain import Meeting
from meeting.repository import MeetingRepository
from member.domain import Member
from member.repository import MemberRepository
from payment.domain import Payment
from payment.repository import PaymentRepository


class MemberService:
    def __init__(self) -> None:
        self.meeting_repository = MeetingRepository()
        self.member_repository = MemberRepository()
        self.payment_repository = PaymentRepository()

    async def create(self, name, leader, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        member = Member(
            id=None,
            name=name,
            leader=leader,
            meeting_id=meeting_id,
        )
        if member.leader:
            if await self.member_repository.read_list_by_meeting_id(
                member.meeting_id, db_session
            ):
                raise LeaderAlreadyException
        await self.member_repository.create(member, db_session)
        return member

    async def update(self, id, name, leader, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        member = Member(
            id=id,
            name=name,
            leader=leader,
            meeting_id=meeting_id,
        )
        if member.leader:
            pre_leader_member = (
                await self.member_repository.read_leader_member_by_meeting_id(
                    member.meeting_id, db_session
                )
            )
            pre_leader_member.leader = False
            await self.member_repository.update(pre_leader_member, db_session)
        await self.member_repository.update(member, db_session)

    async def delete(self, member_id, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        member = await self.member_repository.read_by_id(member_id, db_session)
        member.delete_member_if_not_leader()
        payments = await self.payment_repository.read_list_by_meeting_id(
            meeting_id, db_session
        )
        for payment in payments:
            payment.check_in_member(member)
        await self.member_repository.delete(member, db_session)

    async def read(self, meeting_id, user_id, db_session):
        meeting = await self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        members = await self.member_repository.read_list_by_meeting_id(
            meeting_id, db_session
        )
        payments = await self.payment_repository.read_list_by_meeting_id(
            meeting_id, db_session
        )
        if not payments:
            return members

        calculate = Calculate(members=members, payments=payments)
        calculate.split_members()

        return set_DTO(MemberDTO, members)
