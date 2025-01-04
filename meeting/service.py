from fastapi import Depends
from requests import Session

from base.database_connector import get_db_session
from base.exceptions import IncompleteShareExcption, SharePageNotMeetingExcption
from calculate.domain import Calculate
from meeting.domain import Meeting
from meeting.repository import MeetingRepository
from member.repository import MemberRepository
from payment.repository import PaymentRepository
from user.repository import UserRepository


def get_meeting_service(db_session: Session = Depends(get_db_session)):
    return MeetingService(db_session=db_session)


class MeetingService:
    def __init__(self, db_session: Session) -> None:
        self.meeting_repository = MeetingRepository(db_session)
        self.member_repository = MemberRepository(db_session)
        self.payment_repository = PaymentRepository(db_session)
        self.user_repository = UserRepository(db_session)

    def add(self, user_id):
        user = self.user_repository.read_by_user_id(user_id)
        meeting = Meeting.create_template(user_id)
        print(meeting.__dict__)
        meeting.load_user_deposit_information(user)
        self.meeting_repository.create(meeting)
        return meeting

    def create_simple_meeting(self, user_id):
        user = self.user_repository.read_by_user_id(user_id)
        meeting = Meeting.create_simple_template(user_id)
        meeting.load_user_deposit_information(user)
        self.meeting_repository.create(meeting)
        return meeting

    def update_simple_meeting_data(self, meeting_id, user_id, simple_meeting_data_request):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        self.meeting_repository.update_simple_meeting_data(meeting_id, simple_meeting_data_request)

    def edit_information(self, id, user_id, name, date):
        meeting = self.meeting_repository.read_by_id(id)
        meeting.is_user_of_meeting(user_id)
        meeting.update_information(name, date)
        self.meeting_repository.update_information(meeting)

    def edit_kakao_deposit(self, id, user_id, kakao_deposit_id):
        meeting = self.meeting_repository.read_by_id(id)
        meeting.is_user_of_meeting(user_id)
        meeting.update_kakao_deposit_information(kakao_deposit_id)
        self.meeting_repository.update_kakao_deposit(meeting)

    def edit_toss_deposit(self, id, user_id, bank, account_number):
        meeting = self.meeting_repository.read_by_id(id)
        meeting.is_user_of_meeting(user_id)
        meeting.update_toss_deposit_information(bank, account_number)
        self.meeting_repository.update_toss_deposit(meeting)

    def remove(self, id, user_id):
        meeting = self.meeting_repository.read_by_id(id)
        meeting.is_user_of_meeting(user_id)
        if meeting.is_simple:
            self.meeting_repository.delete(meeting)
            self.meeting_repository.delete_simple_meeting_data(meeting.id)
        else:
            self.meeting_repository.delete(meeting)
            self.member_repository.delete_by_meeting_id(meeting.id)
            self.payment_repository.delete_by_meeting_id(meeting.id)

    def read(self, id, user_id):
        meeting = self.meeting_repository.read_by_id(id)
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    def read_simple_meeting(self, meeting_id, user_id):
        meeting = self.meeting_repository.read_by_id(meeting_id)
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    def read_meetings(self, user_id):
        meetings = self.meeting_repository.read_list_by_user_id(user_id)
        return meetings

    def read_share_page(self, uuid):
        meeting = self.meeting_repository.read_by_uuid(uuid)
        if not meeting:
            raise SharePageNotMeetingExcption
        if meeting.is_simple:
            return {"meeting": meeting}
        else:
            members = self.member_repository.read_list_by_meeting_id(meeting.id)
            payments = self.payment_repository.read_list_by_meeting_id(meeting.id)
            if not members or not payments:
                raise IncompleteShareExcption

            calculate = Calculate(members=members, payments=payments)
            calculate.split_payments()
            calculate.split_members()

            for member in members:
                member.create_deposit_link(meeting)
            return {"meeting": meeting, "members": members, "payments": payments}
