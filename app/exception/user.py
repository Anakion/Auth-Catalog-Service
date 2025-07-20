class UserNotFoundException(Exception):
    detail = "User not found"


class UserNotCorrectPasswordException(Exception):
    detail = "User not correct password"


class TokenNotCorrectException(Exception):
    detail = "Token is not correct"


class TokenExpiredException(Exception):
    detail = "Token has expired"
