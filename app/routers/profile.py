from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from app.core.config import get_config_settings
from app.routers import RouterTags

router = APIRouter(
    tags=[RouterTags.Profile],
)

settings = get_config_settings()
templates = Jinja2Templates(directory=settings.template_root)


@router.get("/profiles", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
