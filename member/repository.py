from sqlalchemy.orm import Session

from base.database_model import MemberModel
from member.domain import Member


class MemberRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, member: Member):
        member_model = MemberModel(
            id=None,
            name=member.name,
            leader=member.leader,
            meeting_id=member.meeting_id,
        )
        self.db_session.add(member_model)
        self.db_session.commit()
        member.id = member_model.id

    def update(self, member: Member):
        member_model = self.db_session.query(MemberModel).filter(MemberModel.id == member.id).first()
        member_model.name = member.name
        member_model.leader = member.leader
        self.db_session.commit()

    def delete(self, member: Member, db_session: Session):
        member_model = self.db_session.query(MemberModel).filter(MemberModel.id == member.id).first()
        self.db_session.delete(member_model)
        self.db_session.commit()

    def read_by_id(self, member_id):
        member_model = self.db_session.query(MemberModel).filter(MemberModel.id == member_id).first()
        if not member_model:
            return None
        member = Member(
            id=member_model.id,
            name=member_model.name,
            leader=member_model.leader,
            meeting_id=member_model.meeting_id,
        )
        return member

    def read_list_by_meeting_id(self, meeting_id):
        members = list()
        member_models = self.db_session.query(MemberModel).filter(MemberModel.meeting_id == meeting_id).all()
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

    def read_leader_member_by_meeting_id(self, meeting_id):
        member_model = self.db_session.query(MemberModel).filter(MemberModel.meeting_id == meeting_id).filter(MemberModel.leader == True).first()
        if not member_model:
            return None
        member = Member(
            id=member_model.id,
            name=member_model.name,
            leader=member_model.leader,
            meeting_id=member_model.meeting_id,
        )
        return member

    def delete_by_meeting_id(self, meeting_id):
        self.db_session.query(MemberModel).filter(MemberModel.meeting_id == meeting_id).delete()
        self.db_session.commit()
