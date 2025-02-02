import json

from sqlalchemy import case, nulls_last
from sqlalchemy.orm import Session

from base.database_model import PaymentModel
from payment.domain import Payment


def _json_encoding_attend_member_ids(attend_member_ids):
    encode_data = json.dumps(attend_member_ids)
    return encode_data


def _json_decoding_attend_member_ids(attend_member_ids):
    decode_data = json.loads(attend_member_ids)
    return decode_data


class PaymentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, payment: Payment):
        payment_model = PaymentModel(
            id=None,
            place=payment.place,
            price=payment.price,
            pay_member_id=payment.pay_member_id,
            attend_member_ids=_json_encoding_attend_member_ids(payment.attend_member_ids),
            meeting_id=payment.meeting_id,
        )
        self.db_session.add(payment_model)
        self.db_session.commit()
        payment.id = payment_model.id

    def update(self, payment: Payment):
        payment_model = self.db_session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
        payment_model.place = payment.place
        payment_model.price = payment.price
        payment_model.pay_member_id = payment.pay_member_id
        payment_model.attend_member_ids = _json_encoding_attend_member_ids(payment.attend_member_ids)
        self.db_session.commit()

    def delete(self, payment: Payment):
        payment_model = self.db_session.query(PaymentModel).filter(PaymentModel.id == payment.id).first()
        self.db_session.delete(payment_model)
        self.db_session.commit()

    def read_list_by_meeting_id(self, meeting_id) -> list[Payment]:
        payments = list()
        payment_models = (
            self.db_session.query(PaymentModel)
            .filter(PaymentModel.meeting_id == meeting_id)
            .order_by(
                case((PaymentModel.order_no == None, 1), else_=0),
            )
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
                attend_member_ids=_json_decoding_attend_member_ids(payment_model.attend_member_ids),
                meeting_id=payment_model.meeting_id,
            )
            payments.append(payment)
        return payments

    def delete_by_meeting_id(self, meeting_id):
        self.db_session.query(PaymentModel).filter(PaymentModel.meeting_id == meeting_id).delete()
        self.db_session.commit()

    def update_order(self, payment_order_data):
        for index, payment_id in enumerate(payment_order_data):
            self.db_session.query(PaymentModel).filter(PaymentModel.id == payment_id).update({"order_no": index})
        self.db_session.commit()
