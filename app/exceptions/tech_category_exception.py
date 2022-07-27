from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class TechCategoryException(Exception):
    pass


class DuplicateTechCategoryName(TechCategoryException):
    def __init__(self, name: str):
        self.name = name


async def user_duplicate_tech_category_name_handler(request: Request, e: DuplicateTechCategoryName):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"{e.name} is duplicated"}
    )
