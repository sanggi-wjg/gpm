from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class NotFound(Exception):
    pass


async def not_found_handler(request: Request, e: NotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found"}
    )


class DuplicateError(Exception):
    def __init__(self, thing: str):
        self.thing = thing


async def duplicate_error_handler(request: Request, e: DuplicateError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"{e.thing} is duplicated"}
    )
