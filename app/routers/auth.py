from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import get_config_settings
from app.database.database import get_db
from app.exceptions.user_exception import BadCredentials, NotExistEmail
from app.service import user_service
from app.routers import RouterTags
from app.schemas.auth_schema import Token, TokenData
from app.utils.auth_utils import verify_password, create_jwt_access_token

router = APIRouter(
    tags=[RouterTags.Auth],
    responses={404: {"detail": "not found"}}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def verify_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        settings = get_config_settings()
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


@router.post("/login", response_model=Token)
async def login_for_jwt_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    find_user = user_service.find_user_by_email(db, form_data.username)
    if not find_user:
        raise NotExistEmail(form_data.username)
    if not verify_password(form_data.password, find_user.hashed_password):
        raise BadCredentials()

    jwt_token = create_jwt_access_token(data={"sub": find_user.email})
    return Token(access_token=jwt_token, token_type="bearer")
