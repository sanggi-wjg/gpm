from fastapi import Request, status
from starlette.responses import JSONResponse


class UserException(Exception):
    pass


class DuplicateEmail(UserException):
    def __init__(self, email: str):
        self.email = email


async def user_duplicate_email_handler(request: Request, e: DuplicateEmail):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"{e.email} is duplicated"}
    )


class UserNotFound(UserException):
    pass


async def user_not_found_handler(request: Request, e: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"}
    )
