from typing import List

from pydantic import BaseModel, AnyHttpUrl, validator


class SocialSite(BaseModel):
    site_name: str
    site_url: AnyHttpUrl
    site_user_name: str

    @validator("site_url")
    def site_url_must_contain(cls, v):
        if '{input}' not in v:
            raise ValueError("invalid site url")
        return v


class UserTech(BaseModel):
    tech_category_name: str
    tech_stack_name: str
    tech_stack_color: str | None = ''


class UserMarkdownCreate(BaseModel):
    user_github_name: str
    user_introduction: str | None = ''
    user_socials: List[SocialSite] | List[None] = []
    user_techs: List[UserTech] | List[None] = []

    @validator("user_techs")
    def replace_tech_stack_name(cls, user_techs):
        for tech in user_techs:
            tech.tech_stack_name = tech.tech_stack_name.replace(" ", '')
        return user_techs
