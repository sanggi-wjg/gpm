import os

from app.schemas.markdown_schema import SocialSite
from app.service.markdown.converters import convert_hello, convert_introduction, SocialConverter
from app.service.markdown.markdown_converter import get_markdown_save_path, save_markdown


class TestMarkdownConverter:

    def test_get_markdown_save_path(self):
        # given
        user_github_name = "Test"
        # when
        save_path = get_markdown_save_path(user_github_name)
        # then
        assert save_path
        assert f"{user_github_name}.md" in save_path

    def test_save_markdown(self):
        # given
        user_github_name = "Test"
        content = "Hello!"
        # when
        file_path = save_markdown(user_github_name, content)
        # then
        assert file_path
        assert f"{user_github_name}.md" in file_path
        assert os.path.exists(file_path)

    def test_convert_hello(self):
        # given
        user_name = "Test"
        # when
        result = convert_hello(user_name)
        # then
        assert result
        # assert result == f"""# 안녕하세요 [{user_name}](https://github.com/{user_name}) 입니다! <img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=50px>"""

    def test_convert_introduction(self):
        # given
        user_introduction = "Test"
        # when
        result = convert_introduction(user_introduction)
        # then
        assert result

    def get_sample_socials(self):
        return [
            SocialSite(site_name="Tistory", site_url="https://{input}.tistory.com/", site_user_name="test"),
            SocialSite(site_name="Instagram", site_url="https://instagram.com/{input}", site_user_name="test"),
        ]

    def test_social_converter(self):
        # given
        converter = SocialConverter()

        # when
        result = converter.convert(self.get_sample_socials())
        print(result)

        # then
        assert result
