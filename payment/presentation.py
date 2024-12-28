from base.database_connector import get_db_session
from base.exceptions import catch_exception
from base.token import Token
from fastapi import APIRouter, Depends, Header
from payment.service import PaymentService
from pydantic import BaseModel

payment_service = PaymentService()


class PaymentData(BaseModel):
    place: str
    price: int
    pay_member_id: int
    attend_member_ids: list[int]


class PaymentPresentation:
    router = APIRouter(prefix="/api/meeting/{meeting_id}/payment")

    @router.post("", status_code=201)
    async def create(
        meeting_id,
        payment_data: PaymentData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await payment_service.create(
                place=payment_data.place,
                price=payment_data.price,
                pay_member_id=payment_data.pay_member_id,
                attend_member_ids=payment_data.attend_member_ids,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.get("", status_code=200)
    async def read(
        meeting_id, Authorization=Header(None), db_session=Depends(get_db_session)
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            payments = await payment_service.read(
                meeting_id=meeting_id, user_id=user_id, db_session=db_session
            )
            return payments
        except Exception as e:
            catch_exception(e)

    @router.put("/{payment_id}", status_code=200)
    async def update(
        meeting_id: int,
        payment_id: int,
        payment_data: PaymentData,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await payment_service.update(
                id=payment_id,
                place=payment_data.place,
                price=payment_data.price,
                pay_member_id=payment_data.pay_member_id,
                attend_member_ids=payment_data.attend_member_ids,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)

    @router.delete("/{payment_id}", status_code=200)
    async def delete(
        meeting_id: int,
        payment_id: int,
        Authorization=Header(None),
        db_session=Depends(get_db_session),
    ):
        try:
            user_id = Token.get_user_id_by_token(token=Authorization)
            await payment_service.delete(
                id=payment_id,
                meeting_id=meeting_id,
                user_id=user_id,
                db_session=db_session,
            )
        except Exception as e:
            catch_exception(e)
