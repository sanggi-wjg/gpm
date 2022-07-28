from typing import List

from pydantic import BaseModel


# class Markdown(BaseModel):
#     content: str


class UserMarkdownCreate(BaseModel):
    user_github_name: str | None = None
    user_introduction: str | None = None
    user_socials: List[str] | List[None] = []
    user_tech_stacks: List[str] | List[None] = []
