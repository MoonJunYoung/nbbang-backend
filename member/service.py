from fastapi import Depends
from requests import Session

from base.database_connector import get_db_session
from base.dto import MemberDTO, set_DTO
from base.exceptions import LeaderAlreadyException
from calculate.domain import Calculate
from meeting.repository import MeetingRepository
from member.domain import Member
from member.repository import MemberRepository
from payment.repository import PaymentRepository


def get_member_service(db_session: Session = Depends(get_db_session)):
    return MemberService(db_session=db_session)


class MemberService:
    def __init__(self, db_session: Session) -> None:
        self.meeting_repository = MeetingRepository(db_session)
        self.member_repository = MemberRepository(db_session)
        self.payment_repository = PaymentRepository(db_session)

    def create(self, name, leader, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        member = Member(
            id=None,
            name=name,
            leader=leader,
            meeting_id=meeting_id,
        )
        if member.leader:
            if self.member_repository.read_list_by_meeting_id(member.meeting_id):
                raise LeaderAlreadyException
        self.member_repository.create(member)
        return member

    def update(self, id, name, leader, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        member = Member(
            id=id,
            name=name,
            leader=leader,
            meeting_id=meeting_id,
        )
        if member.leader:
            pre_leader_member = self.member_repository.read_leader_member_by_meeting_id(member.meeting_id)
            pre_leader_member.leader = False
            self.member_repository.update(pre_leader_member)
        self.member_repository.update(member)

    def delete(self, member_id, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        member = self.member_repository.read_by_id(member_id)
        member.delete_member_if_not_leader()
        payments = self.payment_repository.read_list_by_meeting_id(meeting_id)
        for payment in payments:
            payment.check_in_member(member)
        self.member_repository.delete(member)

    def read(self, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        members = self.member_repository.read_list_by_meeting_id(meeting_id)
        payments = self.payment_repository.read_list_by_meeting_id(meeting_id)
        if not payments:
            return members

        calculate = Calculate(members=members, payments=payments)
        calculate.split_members()

        return set_DTO(MemberDTO, members)
