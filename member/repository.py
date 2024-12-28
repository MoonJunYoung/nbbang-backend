from base.database_connector import MysqlCRUDTemplate
from base.database_model import MemberModel
from member.domain import Member
from sqlalchemy.orm import Session


class MemberRepository:
    async def create(self, member: Member, db_session: Session):
        member_model = MemberModel(
            id=None,
            name=member.name,
            leader=member.leader,
            meeting_id=member.meeting_id,
        )
        db_session.add(member_model)
        db_session.commit()
        member.id = member_model.id

    async def update(self, member: Member, db_session: Session):
        member_model = (
            db_session.query(MemberModel).filter(MemberModel.id == member.id).first()
        )
        member_model.name = member.name
        member_model.leader = member.leader
        db_session.commit()

    async def delete(self, member: Member, db_session: Session):
        member_model = (
            db_session.query(MemberModel).filter(MemberModel.id == member.id).first()
        )
        db_session.delete(member_model)
        db_session.commit()

    async def read_by_id(self, member_id, db_session: Session):
        member_model = (
            db_session.query(MemberModel).filter(MemberModel.id == member_id).first()
        )
        if not member_model:
            return None
        member = Member(
            id=member_model.id,
            name=member_model.name,
            leader=member_model.leader,
            meeting_id=member_model.meeting_id,
        )
        return member

    async def read_list_by_meeting_id(self, meeting_id, db_session: Session):
        members = list()
        member_models = (
            db_session.query(MemberModel)
            .filter(MemberModel.meeting_id == meeting_id)
            .all()
        )
        if not member_models:
            return members
        for member_model in member_models:
            member = Member(
                id=member_model.id,
                name=member_model.name,
                leader=member_model.leader,
                meeting_id=member_model.meeting_id,
            )
            members.append(member)
        members = self.__sort_leader(members)
        return members

    def __sort_leader(self, members: list[Member]):
        for member in members:
            if member.leader:
                members.remove(member)
                members.insert(0, member)
        return members

    async def read_leader_member_by_meeting_id(self, meeting_id, db_session: Session):
        member_model = (
            db_session.query(MemberModel)
            .filter(MemberModel.meeting_id == meeting_id)
            .filter(MemberModel.leader == True)
            .first()
        )
        if not member_model:
            return None
        member = Member(
            id=member_model.id,
            name=member_model.name,
            leader=member_model.leader,
            meeting_id=member_model.meeting_id,
        )
        return member

    async def delete_by_meeting_id(self, meeting_id, db_session: Session):
        db_session.query(MemberModel).filter(
            MemberModel.meeting_id == meeting_id
        ).delete()
        db_session.commit()
