import uuid

import requests
from fastapi import Depends, APIRouter, Request
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from app.core.config import get_config_settings
from app.database.database import get_db
from app.database.models import UserProvider, UserEntity
from app.exceptions.user_exception import BadCredentials, NotExistEmail
from app.routers.home import templates
from app.schemas.user_schema import UserProvidedRegister
from app.service import user_service
from app.routers import RouterTags
from app.schemas.auth_schema import Token, TokenData, GithubToken
from app.utils.authentication import verify_password, create_jwt_access_token

router = APIRouter(
    tags=[RouterTags.Auth],
    responses={404: {"detail": "not found"}}
)

settings = get_config_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserEntity:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.access_token_algorithm])
        username = payload.get('sub')
        if username is None:
            raise BadCredentials()
        token_data = TokenData(user_email=username)
    except JWTError:
        raise BadCredentials()

    find_user = user_service.find_user_by_email(db, token_data.user_email)
    if not find_user:
        raise BadCredentials()
    return find_user


async def verify_admin_user(user: UserEntity = Depends(verify_current_user)) -> UserEntity:
    if not user.is_admin:
        raise BadCredentials()

    return user


@router.post("/token", response_model=Token)
async def get_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    find_user = user_service.find_user_by_email(db, form_data.username)
    if not find_user:
        raise NotExistEmail(form_data.username)
    if not verify_password(form_data.password, find_user.hashed_password):
        raise BadCredentials()

    jwt_token = create_jwt_access_token(data={"sub": find_user.email})
    return Token(access_token=jwt_token, token_type="bearer")


@router.get("/join", response_class=HTMLResponse)
async def user_join_page(request: Request):
    return templates.TemplateResponse("join.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/login/github")
async def login_github_redirect():
    query = f"?client_id={settings.github_client_id}"
    query += f"&state={uuid.uuid4()}"
    return RedirectResponse(f"https://github.com/login/oauth/authorize{query}")


@router.get("/login/github/callback")
async def login_github_callback(request: Request, code: str, state: str = None, db: Session = Depends(get_db)):
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data=jsonable_encoder({
            'client_id': settings.github_client_id,
            'client_secret': settings.github_secret,
            'code': code,
        }),
        headers={"Accept": "application/json"}
    )
    if response.status_code != status.HTTP_200_OK:
        raise BadCredentials()
    github_token = GithubToken(**response.json(), state=state)

    response = requests.get("https://api.github.com/user", headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': f"{github_token.token_type} {github_token.access_token}"
    })
    if response.status_code != status.HTTP_200_OK:
        raise BadCredentials()

    user_email = response.json()['email']
    find_user = user_service.find_user_by_email_and_provider(db, user_email, UserProvider.GITHUB)
    if not find_user:
        user_service.create_provider_user(
            db, UserProvidedRegister(email=user_email, provider=UserProvider.GITHUB)
        )

    redirect = RedirectResponse("/")
    redirect.set_cookie("access_token", create_jwt_access_token(data={"sub": user_email}))
    return redirect
