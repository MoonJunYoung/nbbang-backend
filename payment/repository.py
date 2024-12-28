import json

from base.database_connector import MysqlCRUDTemplate
from base.database_model import PaymentModel
from payment.domain import Payment
from sqlalchemy.orm import Session


def _json_encoding_attend_member_ids(attend_member_ids):
    encode_data = json.dumps(attend_member_ids)
    return encode_data


def _json_decoding_attend_member_ids(attend_member_ids):
    decode_data = json.loads(attend_member_ids)
    return decode_data


class PaymentRepository:
    async def create(self, payment: Payment, db_session: Session):
        payment_model = PaymentModel(
            id=None,
            place=payment.place,
            price=payment.price,
            pay_member_id=payment.pay_member_id,
            attend_member_ids=_json_encoding_attend_member_ids(
                payment.attend_member_ids
            ),
            meeting_id=payment.meeting_id,
        )
        db_session.add(payment_model)
        db_session.commit()
        payment.id = payment_model.id

    async def update(self, payment: Payment, db_session: Session):
        payment_model = (
            db_session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
        )
        payment_model.place = payment.place
        payment_model.price = payment.price
        payment_model.pay_member_id = payment.pay_member_id
        payment_model.attend_member_ids = _json_encoding_attend_member_ids(
            payment.attend_member_ids
        )
        db_session.commit()

    async def delete(self, payment: Payment, db_session: Session):
        payment_model = (
            db_session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
        )
        db_session.delete(payment_model)
        db_session.commit()

    async def read_list_by_meeting_id(
        self, meeting_id, db_session: Session
    ) -> list[Payment]:
        payments = list()
        payment_models = (
            db_session.query(PaymentModel)
            .filter(PaymentModel.meeting_id == meeting_id)
            .all()
        )
        if not payment_models:
            return payments
        for payment_model in payment_models:
            payment = Payment(
                id=payment_model.id,
                place=payment_model.place,
                price=payment_model.price,
                pay_member_id=payment_model.pay_member_id,
                attend_member_ids=_json_decoding_attend_member_ids(
                    payment_model.attend_member_ids
                ),
                meeting_id=payment_model.meeting_id,
            )
            payments.append(payment)
        return payments

    async def delete_by_meeting_id(self, meeting_id, db_session: Session):
        db_session.query(PaymentModel).filter(
            PaymentModel.meeting_id == meeting_id
        ).delete()
        db_session.commit()
