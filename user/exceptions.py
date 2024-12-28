from base.exceptions import CustomException


class IdentifierAlreadyException(CustomException):
    def __init__(self, identifier) -> None:
        super().__init__(f"sign-up {identifier} this idnetifier is already")

    status_code = 409
    detail = "this idnetifier is already."


class IdentifierNotFoundException(CustomException):
    def __init__(self, identifier) -> None:
        super().__init__(f"sign-in identifier:{identifier} is not found.")

    status_code = 401
    detail = "incorrect identifier or password."


class PasswordNotMatchException(CustomException):
    def __init__(self, identifier, password) -> None:
        super().__init__(
            f"sign-in password:{password} is not match to identifier:{identifier}."
        )

    status_code = 401
    detail = "incorrect identifier or password."
