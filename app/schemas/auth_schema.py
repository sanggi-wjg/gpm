from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(..., min_length=1, title="Access Token")
    token_type: str = Field(..., min_length=1, title="Token Type")


class TokenData(BaseModel):
    user_email: str | None = None


class GithubToken(BaseModel):
    access_token: str
    scope: str
    token_type: str
    state: str | None = None
