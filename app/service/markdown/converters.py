import random
from typing import List, Callable

from app.core.config import get_config_settings
from app.schemas.markdown_schema import SocialSite, UserTech

settings = get_config_settings()


def convert_hello(user_github_name: str) -> str:
    result = f"# 안녕하세요! [{user_github_name}](https://github.com/{user_github_name}) 입니다! "
    result += '<img src="https://raw.githubusercontent.com/MartinHeinz/MartinHeinz/master/wave.gif" width=40px>'
    return f"{result}\n\n"


def convert_introduction(user_introduction: str) -> str:
    result = "# 💫 About Me\n"
    result += user_introduction.replace('\n', "\\\n")
    return f"{result}\n\n"


def convert_github(user_github_name: str) -> str:
    result = "# 💛 GitHub Statistics\n"
    result += f"![](https://github-readme-stats.vercel.app/api?username={user_github_name}&theme=dark&hide_border=false&include_all_commits=false&count_private=true)\n"
    result += f"![](https://github-readme-streak-stats.herokuapp.com/?user={user_github_name}&theme=dark&hide_border=false)\n"
    result += f"![](https://github-readme-stats.vercel.app/api/top-langs/?username={user_github_name}&theme=dark&hide_border=false&include_all_commits=false&count_private=true&layout=compact)\n\n"
    result += "<br><br>\n"

    result += "# 🏆 GitHub Trophies\n"
    result += f"![](https://github-profile-trophy.vercel.app/?username={user_github_name}&theme=discord&no-frame=false&no-bg=true&margin-w=4)\n"
    return f"{result}\n"


def get_shield_badge(name: str, color: str, logo: str, **kwargs) -> str:
    style = kwargs.get('style', 'for-the-badge')
    logo_color = kwargs.get('logo_color', 'white')
    return f"https://img.shields.io/badge/{name}-{color}.svg?style={style}&logo={logo}&logoColor={logo_color}"


def get_random_colors() -> str:
    colors = (
        'brightgreen', 'green', 'yellowgreen', 'orange', 'red', 'blue', 'success', 'important',
        'informational', 'ff69b4', '9cf', 'violet', 'blueviolet', 'a2d2ff', 'ffafcc', 'fb5607',
        'fefae0', 'ff99c8', 'fcf6bd', 'd0f4de', 'a9def9', 'e4c1f9'
    )
    return colors[random.randint(0, len(colors) - 1)]


class Converter:

    def __init__(self):
        self.shield_badge: Callable = get_shield_badge


class SocialConverter(Converter):

    def create_badge(self, social: SocialSite) -> str:
        badge = f"[![{social.site_name}]({self.shield_badge(social.site_name, get_random_colors(), social.site_name)})]"
        link = f"({social.site_url.replace('{input}', social.site_user_name)})"
        return f"{badge}{link}\n"

    def convert(self, user_socials: List[SocialSite]) -> str:
        result = "## 💌 Socials\n"
        for social in user_socials:
            result += self.create_badge(social)
        return f"{result}<br><br>\n\n"


class TechConverter(Converter):

        def map_by_category_name(self, user_tech: List[UserTech]) -> dict:
        badges = {}
        for tech in user_tech:
            category_name = tech.tech_category_name
            stack_name = tech.tech_stack_name
            stack_color = tech.tech_stack_color

            if category_name not in badges.keys():
                badges.setdefault(category_name, [(stack_name, stack_color)])
            else:
                badges[category_name].append((stack_name, stack_color))
        return badges

    def create_badge(self, stack_name: str, stack_color: str):
        if stack_color:
            return f"![{stack_name}]({self.shield_badge(stack_name, stack_color, stack_name)})\n"
        else:
            return f"![{stack_name}]({self.shield_badge(stack_name, get_random_colors(), stack_name)})\n"

    def convert(self, user_techs: List[UserTech]) -> str:
        result = "# 🛠 Tech Stack\n"
        user_tech_map = self.map_by_category_name(user_techs)

        for category_name, tech_stacks in user_tech_map.items():
            result += f"## {category_name}\n"
            for stack_name, stack_color in tech_stacks:
                result += self.create_badge(stack_name, stack_color)
            result += "\n"
        return f"{result}<br><br>\n\n"
