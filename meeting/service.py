from base.exceptions import IncompleteShareExcption, SharePageNotMeetingExcption
from calculate.domain import Calculate
from meeting.domain import Meeting
from meeting.repository import MeetingRepository
from member.repository import MemberRepository
from payment.repository import PaymentRepository
from user.repository import UserRepository


class MeetingService:
    def __init__(self) -> None:
        self.meeting_repository = MeetingRepository()
        self.member_repository = MemberRepository()
        self.payment_repository = PaymentRepository()
        self.user_repository = UserRepository()

    def add(self, user_id, db_session):
        user = self.user_repository.read_by_user_id(user_id, db_session)
        meeting = Meeting.create_template(user_id)
        meeting.load_user_deposit_information(user)
        self.meeting_repository.create(meeting, db_session)
        return meeting

    def create_simple_meeting(self, user_id, db_session):
        user = self.user_repository.read_by_user_id(user_id, db_session)
        meeting = Meeting.create_simple_template(user_id)
        meeting.load_user_deposit_information(user)
        self.meeting_repository.create(meeting, db_session)
        return meeting

    def update_simple_meeting_data(self, meeting_id, user_id, simple_meeting_data_request, db_session):
        meeting = self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        self.meeting_repository.update_simple_meeting_data(meeting_id, simple_meeting_data_request, db_session)

    def edit_information(self, id, user_id, name, date, db_session):
        meeting = self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_information(name, date)
        self.meeting_repository.update_information(meeting, db_session)

    def edit_kakao_deposit(self, id, user_id, kakao_deposit_id, db_session):
        meeting = self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_kakao_deposit_information(kakao_deposit_id)
        self.meeting_repository.update_kakao_deposit(meeting, db_session)

    def edit_toss_deposit(self, id, user_id, bank, account_number, db_session):
        meeting = self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.update_toss_deposit_information(bank, account_number)
        self.meeting_repository.update_toss_deposit(meeting, db_session)

    def remove(self, id, user_id, db_session):
        meeting = self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        if meeting.is_simple:
            self.meeting_repository.delete(meeting, db_session)
            self.meeting_repository.delete_simple_meeting_data(meeting.id, db_session)
        else:
            self.meeting_repository.delete(meeting, db_session)
            self.member_repository.delete_by_meeting_id(meeting.id, db_session)
            self.payment_repository.delete_by_meeting_id(meeting.id, db_session)

    def read(self, id, user_id, db_session):
        meeting = self.meeting_repository.read_by_id(id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    def read_simple_meeting(self, meeting_id, user_id, db_session):
        meeting = self.meeting_repository.read_by_id(meeting_id, db_session)
        meeting.is_user_of_meeting(user_id)
        meeting.create_share_link()
        return meeting

    def read_meetings(self, user_id, db_session):
        meetings = self.meeting_repository.read_list_by_user_id(user_id, db_session)
        return meetings

    def read_share_page(self, uuid, db_session):
        meeting = self.meeting_repository.read_by_uuid(uuid, db_session)
        if not meeting:
            raise SharePageNotMeetingExcption
        if meeting.is_simple:
            return {"meeting": meeting}
        else:
            members = self.member_repository.read_list_by_meeting_id(meeting.id, db_session)
            payments = self.payment_repository.read_list_by_meeting_id(meeting.id, db_session)
            if not members or not payments:
                raise IncompleteShareExcption

            calculate = Calculate(members=members, payments=payments)
            calculate.split_payments()
            calculate.split_members()

            for member in members:
                member.create_deposit_link(meeting)
            return {"meeting": meeting, "members": members, "payments": payments}
