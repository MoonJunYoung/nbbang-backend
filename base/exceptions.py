import logging
import traceback

from fastapi import HTTPException, Request

logging.basicConfig(filename="./error.log", level=logging.ERROR)
logging.error(traceback.format_exc())


def catch_exception(exce, requests: Request = None):
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
        self.detail = "유효하지 않은 인증 토큰입니다."


class MissingTokenException(CustomException):
    def __init__(self) -> None:
        self.status_code = 401
        self.detail = "인증 토큰이 없습니다."


class MeetingUserMismatchException(CustomException):
    def __init__(self, user_id, meeting_id) -> None:
        self.status_code = 403
        self.detail = f"{user_id} 사용자는 {meeting_id} 모임의 관리자가 아닙니다."


class LeaderAlreadyException(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "이미 리더가 있습니다."


class PaymentInMemberDeleteExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "결제내역에 포홤된 멤버는 삭제할 수 없습니다."


class MemberIsLeaderDeleteExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 409
        self.detail = "리더 멤버는 삭제할 수 없습니다."


class SharePageNotMeetingExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 404
        self.detail = "공유된 정산이 삭제되었거나 유효하지 않습니다."


class IncompleteShareExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 204
        self.detail = "공유된 정산은 완료되지 않았습니다."


class NotAgerrmentExcption(CustomException):
    def __init__(self) -> None:
        self.status_code = 403
        self.detail = "이용약관에 동의해야합니다."


class IdentifierAlreadyException(CustomException):
    def __init__(self, identifier) -> None:
        self.status_code = 409
        self.detail = "이미 사용중인 아이디입니다."


class IdentifierNotFoundException(CustomException):
    def __init__(self, identifier) -> None:
        self.status_code = 401
        self.detail = "아이디 또는 비밀번호가 일치하지 않습니다."


class PasswordNotMatchException(CustomException):
    def __init__(self, identifier, password) -> None:
        self.status_code = 401
        self.detail = "아이디 또는 비밀번호가 일치하지 않습니다."
