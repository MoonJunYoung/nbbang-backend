from base.database_model import MeetingModel
from meeting.domain import Meeting
from sqlalchemy.orm import Session


class MeetingRepository:
    async def create(self, meeting: Meeting, db_session: Session):
        meeting_model = MeetingModel(
            id=None,
            name=meeting.name,
            date=meeting.date,
            user_id=meeting.user_id,
            uuid=meeting.uuid,
            account_number=meeting.toss_deposit_information.account_number,
            bank=meeting.toss_deposit_information.bank,
            kakao_deposit_id=meeting.kakao_deposit_information.kakao_deposit_id,
        )
        db_session.add(meeting_model)
        db_session.commit()
        meeting.id = meeting_model.id

    async def update_information(self, meeting: Meeting, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        )
        meeting_model.name = meeting.name
        meeting_model.date = meeting.date
        db_session.commit()

    async def update_toss_deposit(self, meeting: Meeting, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        )
        meeting_model.bank = meeting.toss_deposit_information.bank
        meeting_model.account_number = meeting.toss_deposit_information.account_number
        db_session.commit()

    async def update_kakao_deposit(self, meeting: Meeting, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        )
        meeting_model.kakao_deposit_id = (
            meeting.kakao_deposit_information.kakao_deposit_id
        )
        db_session.commit()

    async def delete(self, meeting: Meeting, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel).filter(MeetingModel.id == meeting.id).first()
        )
        db_session.delete(meeting_model)
        db_session.commit()

    async def read_list_by_user_id(self, user_id, db_session: Session) -> list[Meeting]:
        meetings = list()
        meeting_models = (
            db_session.query(MeetingModel)
            .filter(MeetingModel.user_id == user_id)
            .order_by(MeetingModel.id.desc())
            .all()
        )
        if not meeting_models:
            return meetings
        for meeting_model in meeting_models:
            meeting = Meeting(
                id=meeting_model.id,
                name=meeting_model.name,
                date=meeting_model.date,
                user_id=meeting_model.user_id,
                uuid=meeting_model.uuid,
            )
            meetings.append(meeting)
        return meetings

    async def read_by_id(self, meeting_id, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel).filter(MeetingModel.id == meeting_id).first()
        )
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
        )
        return meeting

    async def read_by_uuid(self, meeting_uuid, db_session: Session):
        meeting_model = (
            db_session.query(MeetingModel)
            .filter(MeetingModel.uuid == meeting_uuid)
            .first()
        )
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
        )
        return meeting
