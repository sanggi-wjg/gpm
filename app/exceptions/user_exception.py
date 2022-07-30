from fastapi import Request, status
from starlette.responses import JSONResponse


class UserException(Exception):
    pass


class NotExistEmail(UserException):

    def __init__(self, email):
        self.email = email


async def not_exist_email_handler(request: Request, e: NotExistEmail):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": f"Incorrect email: {e.email}"}
    )


class BadCredentials(UserException):
    pass


async def bad_credentials_handler(request: Request, e: BadCredentials):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials"},
        headers={"WWW-Authenticate": "Bearer"}
    )
