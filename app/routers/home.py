from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.config import get_config_settings
from app.routers import RouterTags

settings = get_config_settings()

router = APIRouter(
    tags=[RouterTags.Home],
)

templates = Jinja2Templates(directory=settings.template_root)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
