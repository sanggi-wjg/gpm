from typing import List

from app.schemas.markdown_schema import SocialSite


def convert_hello(user_github_name: str) -> str:
    result = f"# 안녕하세요 [{user_github_name}](https://github.com/{user_github_name}) 입니다! "
    result += '<img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=50px>'
    return f"{result}\n\n"


def convert_introduction(user_introduction: str) -> str:
    result = "# 💫 About Me :\n"
    result += user_introduction.replace('\n', "\\\n")
    return f"{result}\n\n"


class SocialConverter:

    def __init__(self):
        self.social_sites = {
            'Instagram': "https://img.shields.io/badge/Instagram-ff69b4.svg?logo=Instagram&logoColor=white",
            'Tistory': "https://img.shields.io/badge/Tistory-orange.svg?logo=Tistory&logoColor=white",
            'GitHub': "https://img.shields.io/badge/GitHub-black.svg?logo=GitHub&logoColor=white",
            'NaverBlog': "https://img.shields.io/badge/NaverBlog-green.svg?logo=NaverBlog&logoColor=white",
        }

    def parse(self, social: SocialSite) -> str:
        badge = f"[![{social.site_name}]({self.social_sites.get(social.site_name, '')})]"
        link = f"({social.site_url.replace('{input}', social.site_user_name)})"
        return f"{badge}{link}\n"

    def convert(self, user_socials: List[SocialSite]) -> str:
        result = "## 💌 Socials\n"
        for social in user_socials:
            result += self.parse(social)
        return f"{result}\n\n"
