class CustomException(Exception):
    pass


class AccountLocked(CustomException):
    pass


class AccountSuspended(CustomException):
    pass


class InvalidToken(CustomException):
    pass


class AccountNotFound(CustomException):
    pass


class FollowItSelfError(CustomException):
    pass
