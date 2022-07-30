from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_email: str | None = None


class GithubToken(BaseModel):
    access_token: str
    scope: str
    token_type: str
    state: str | None = None
