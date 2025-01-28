import logging
import traceback

from fastapi import HTTPException, Request

logging.basicConfig(filename="./error.log", level=logging.ERROR)
logging.error(traceback.format_exc())


def catch_exception(exce, requests: Request = None):
    print(exce.__class__, "?????")
    if issubclass(exce.__class__, CustomException):
        logging.error(f"\n===\nA custom error occurred. : {exce}\n===")
        raise HTTPException(status_code=exce.status_code, detail=exce.detail)
    logging.error(f"\n===\nAn unexpected error occurred. : {exce}\ndetail : {traceback.format_exc()}===")
    print(f"\n===\nAn unexpected error occurred. : {exce}\ndetail : {traceback.format_exc()}===")
    raise HTTPException(
        status_code=500,
        detail="An internal server error occurred. If the problem persists, please contact our support team.",
    )


class CustomException(HTTPException):
    pass


# class IdentifierAlreadyException(CustomException):
#     def __init__(self, identifier) -> None:
#         super().__init__(f"sign-up {identifier} this idnetifier is already")

#     status_code = 409
#     detail = "this idnetifier is already."


# class IdentifierNotFoundException(CustomException):
#     def __init__(self, identifier) -> None:
#         super().__init__(f"sign-in identifier:{identifier} is not found.")

#     status_code = 401
#     detail = "incorrect identifier or password."


# class PasswordNotMatchException(CustomException):
#     def __init__(self, identifier, password) -> None:
#         super().__init__(
#             f"sign-in password:{password} is not match to identifier:{identifier}."
#         )

#     status_code = 401
#     detail = "incorrect identifier or password."


class InvalidTokenException(CustomException):
    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "invalid authorization token."


class MissingTokenException(CustomException):
    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "authorization token is missing."


class MeetingUserMismatchException(CustomException):
    def __init__(self, user_id, meeting_id) -> None:
        self.status_code = 403
        self.detail = f"this user:{user_id} does not own the meeting:{meeting_id}."


class LeaderAlreadyException(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "this meeting already has a leader."


class PaymentInMemberDeleteExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "it is not possible to delete the member you want to delete because it is included in the payment."


class MemberIsLeaderDeleteExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "the leader member cannot be deleted."


class SharePageNotMeetingExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "That shared page has been deleted or is invalid"


class IncompleteShareExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 204
        self.detail = "This sharing page is not complete"


class NotAgerrmentExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 403
        self.detail = "need Agreement"
