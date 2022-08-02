import os

from app.schemas.markdown_schema import SocialSite, UserTech, UserMarkdownCreate
from app.service.markdown.converters import convert_hello, convert_introduction, SocialConverter, TechConverter, \
    convert_github
from app.service.markdown.markdown_converter import get_markdown_save_path, save_markdown, MarkdownConverter


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
        user_name = "Test"
        result = convert_hello(user_name)
        assert result
        # assert result == f"""# 안녕하세요 [{user_name}](https://github.com/{user_name}) 입니다! <img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=50px>"""

    def test_convert_introduction(self):
        user_introduction = "Test"
        result = convert_introduction(user_introduction)
        assert result

    def test_convert_github(self):
        user_name = "Test"
        result = convert_github(user_name)
        assert result

    def get_sample_socials(self):
        return [
            SocialSite(site_name="Tistory", site_url="https://{input}.tistory.com/", site_user_name="test"),
            SocialSite(site_name="Instagram", site_url="https://instagram.com/{input}", site_user_name="test"),
        ]

    def test_social_converter(self):
        converter = SocialConverter()
        result = converter.convert(self.get_sample_socials())
        assert result

    def get_sample_user_techs(self):
        return [
            UserTech(tech_category_name='Programming Language', tech_stack_name='PHP'),
            UserTech(tech_category_name='Programming Language', tech_stack_name='Python'),
            UserTech(tech_category_name='Framework', tech_stack_name='Gin'),
            UserTech(tech_category_name='Framework', tech_stack_name='SpringBoot'),
            UserTech(tech_category_name='Database', tech_stack_name='Cubrid'),
            UserTech(tech_category_name='Database', tech_stack_name='MariaDB')
        ]

    def test_tech_converters(self):
        converter = TechConverter()
        result = converter.convert(self.get_sample_user_techs())
        assert result

    def test_markdown_converter(self):
        # given
        markdown_create = UserMarkdownCreate(
            user_github_name="TestUser",
            user_introduction="TestIntroduction",
            user_socials=[
                SocialSite(site_name="TestSiteName", site_url="https://{input}.test.com", site_user_name="TestSiteUser")
            ],
            user_techs=[
                UserTech(tech_category_name="Framework", tech_stack_name="Gin")
            ]
        )
        converter = MarkdownConverter(markdown_create)
        result = converter.convert()
        assert result
