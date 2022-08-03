from enum import Enum


class RouterTags(str, Enum):
    Home = "Home"
    Auth = "Auth"
    User = "Users"
    Tech = "Techs"
    Markdown = "Markdowns"
    Profile = "Profiles"
