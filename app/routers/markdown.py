from fastapi import APIRouter
from starlette import status
from starlette.responses import FileResponse

from app.routers import RouterTags
from app.schemas.markdown_schema import UserMarkdownCreate
from app.service.markdown.markdown_converter import MarkdownConverter, save_markdown

router = APIRouter(
    prefix="/api/v1",
    tags=[RouterTags.Markdown],
    responses={404: {"detail": "not found"}}
)


@router.post("/markdowns", response_class=FileResponse, status_code=status.HTTP_201_CREATED)
async def get_tech_categories(user_markdown: UserMarkdownCreate):
    converter = MarkdownConverter(user_markdown)
    return FileResponse(
        save_markdown(user_markdown.user_github_name, converter.convert()),
        media_type="text/markdown",
        filename=f"{user_markdown.user_github_name}.md",
        status_code=status.HTTP_201_CREATED,
    )
