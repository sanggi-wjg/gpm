from typing import List

from pydantic import BaseModel, AnyHttpUrl, validator


class SocialSite(BaseModel):
    site_name: str
    site_url: AnyHttpUrl
    site_user_name: str

    @validator("site_url")
    def valid_site_url(cls, v):
        if '{input}' not in v:
            raise ValueError("invalid site url")
        return v


class UserTech(BaseModel):
    tech_category_name: str
    tech_stack_name: str


class UserMarkdownCreate(BaseModel):
    user_github_name: str
    user_introduction: str | None = None
    user_socials: List[SocialSite] | List[None] = []
    user_techs: List[UserTech] | List[None] = []
