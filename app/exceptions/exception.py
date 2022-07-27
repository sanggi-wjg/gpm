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
