from typing import List

from app.schemas.markdown_schema import SocialSite


def convert_hello(user_github_name: str) -> str:
    result = f"# 안녕하세요 [{user_github_name}](https://github.com/{user_github_name}) 입니다! "
    result += '<img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=50px>'
    return result


def convert_introduction(user_introduction: str) -> str:
    result = "\n\n# 💫 About Me :\n"
    result += user_introduction.replace('\n', "\\\n")
    return result


class SocialConverter:

    def __init__(self):
        self.social_sites = {
            'Instagram': "https://img.shields.io/badge/Instagram-%23E4405F.svg?logo=Instagram&logoColor=white"
        }

    def convert(self, user_socials: List[SocialSite]) -> str:
        result = "\n## 💌 Socials"
        for social in user_socials:
            print(social)

        return result
