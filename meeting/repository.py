from sqlalchemy.orm import Session

from base.database_model import MeetingModel
from meeting.domain import Meeting
from meeting.presentation import SimpleMeetingDataRequest


class MeetingRepository:
    def create(self, meeting: Meeting, db_session: Session):
        meeting_model = MeetingModel(
            id=None,
            name=meeting.name,
            date=meeting.date,
            user_id=meeting.user_id,
            uuid=meeting.uuid,
            account_number=meeting.toss_deposit_information.account_number,
            bank=meeting.toss_deposit_information.bank,
            kakao_deposit_id=meeting.kakao_deposit_information.kakao_deposit_id,
            is_simple=meeting.is_simple,
        )
        db_session.add(meeting_model)
        db_session.commit()
        meeting.id = meeting_model.id

    def update_information(self, meeting: Meeting, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        meeting_model.name = meeting.name
        meeting_model.date = meeting.date
        db_session.commit()

    def update_simple_meeting_data(self, meeting_id, simple_meeting_data_request: SimpleMeetingDataRequest, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
        if not meeting_model:
            raise Exception("Meeting not found")
        meeting_model.name = simple_meeting_data_request.name
        meeting_model.date = simple_meeting_data_request.date
        meeting_model.simple_price = simple_meeting_data_request.price
        meeting_model.simple_member_count = simple_meeting_data_request.member_count
        db_session.commit()

    def update_toss_deposit(self, meeting: Meeting, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        meeting_model.bank = meeting.toss_deposit_information.bank
        meeting_model.account_number = meeting.toss_deposit_information.account_number
        db_session.commit()

    def update_kakao_deposit(self, meeting: Meeting, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        meeting_model.kakao_deposit_id = meeting.kakao_deposit_information.kakao_deposit_id
        db_session.commit()

    def delete(self, meeting: Meeting, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        db_session.delete(meeting_model)
        db_session.commit()

    def delete_simple_meeting_data(self, meeting_id, db_session: Session):
        simple_meeting_data_model = db_session.query(SimpleMeetingDataModel).filter(SimpleMeetingDataModel.meeting_id == meeting_id).first()
        db_session.delete(simple_meeting_data_model)
        db_session.commit()

    def read_list_by_user_id(self, user_id, db_session: Session) -> list[Meeting]:
        meetings = list()
        meeting_models = db_session.query(MeetingModel).filter(MeetingModel.user_id == user_id).order_by(MeetingModel.id.desc()).all()
        if not meeting_models:
            return meetings
        for meeting_model in meeting_models:
            meeting = Meeting(
                id=meeting_model.id,
                name=meeting_model.name,
                date=meeting_model.date,
                user_id=meeting_model.user_id,
                uuid=meeting_model.uuid,
                is_simple=meeting_model.is_simple,
            )
            meetings.append(meeting)
        return meetings

    def read_by_id(self, meeting_id, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
        if not meeting_model:
            return None
        meeting = Meeting(
            id=meeting_model.id,
            name=meeting_model.name,
            date=meeting_model.date,
            user_id=meeting_model.user_id,
            uuid=meeting_model.uuid,
            bank=meeting_model.bank,
            account_number=meeting_model.account_number,
            kakao_deposit_id=meeting_model.kakao_deposit_id,
            is_simple=meeting_model.is_simple,
            simple_price=meeting_model.simple_price,
            simple_member_count=meeting_model.simple_member_count,
        )
        return meeting

    def read_by_uuid(self, meeting_uuid, db_session: Session):
        meeting_model = db_session.query(MeetingModel).filter(MeetingModel.uuid == meeting_uuid).first()
        if not meeting_model:
            return None
        meeting = Meeting(
            id=meeting_model.id,
            name=meeting_model.name,
            date=meeting_model.date,
            user_id=meeting_model.user_id,
            uuid=meeting_model.uuid,
            bank=meeting_model.bank,
            account_number=meeting_model.account_number,
            kakao_deposit_id=meeting_model.kakao_deposit_id,
            is_simple=meeting_model.is_simple,
            simple_price=meeting_model.simple_price,
            simple_member_count=meeting_model.simple_member_count,
        )
        return meeting
