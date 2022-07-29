import os

from app.core.config import get_config_settings
from app.schemas.markdown_schema import UserMarkdownCreate
from app.service.markdown.converters import (
    convert_hello, convert_introduction, SocialConverter, TechConverter,
    convert_github
)


class MarkdownConverter:

    def __init__(self, user_markdown: UserMarkdownCreate):
        self.user_markdown = user_markdown
        self.convert_hello = convert_hello
        self.convert_introduction = convert_introduction
        self.social_converter = SocialConverter()
        self.tech_converter = TechConverter()
        self.convert_github = convert_github

    def convert(self) -> str:
        result = self.convert_hello(self.user_markdown.user_github_name)
        result += self.convert_introduction(self.user_markdown.user_introduction)
        result += self.social_converter.convert(self.user_markdown.user_socials)
        result += self.tech_converter.convert(self.user_markdown.user_techs)
        result += self.convert_github(self.user_markdown.user_github_name)
        return result


settings = get_config_settings()


def get_markdown_save_path(user_github_name: str) -> str:
    return os.path.join(settings.media_root, f"{user_github_name}.md")


def save_markdown(user_github_name: str, content: str) -> str:
    file_path = get_markdown_save_path(user_github_name)
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(content)
    return file_path
