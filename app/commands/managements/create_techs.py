import argparse
import os
import sys
from typing import List, Tuple, Callable

sys.path.append(os.path.abspath('.'))

from app.service import tech_service
from app.service.tech_service import find_or_create_tech_category_by_name
from app.exceptions.exception import DuplicateError
from app.schemas.tech_schema import TechCategoryRegister, TechStackRegister
from app.commands.managements.base_command import BaseCommand


class CreateTechCommand(BaseCommand):
    help: str = "Create tech categories and stacks"

    def add_arguments(self):
        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        funcs: List[Callable] = [
            get_programming_languages, get_frameworks, get_databases, get_infraes, get_mldl, get_others
        ]
        for func in funcs:
            tech_category_register, tech_stack_registers = func()
            self.create_techs(tech_category_register, tech_stack_registers)

    def create_techs(self, tech_category_register: TechCategoryRegister, tech_stack_registers: List[TechStackRegister]):
        tech_category = find_or_create_tech_category_by_name(self.db, tech_category_register)
        self.info(f"Create {tech_category.name} or not")

        for tech_stack in tech_stack_registers:
            try:
                tech_service.create_tech_stack(self.db, tech_category.id, tech_stack)
                self.debug(f"Create {tech_stack.name}")
            except DuplicateError:
                self.warning(f"{tech_stack.name} is exist")


def get_programming_languages() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Programming Language"), [
        TechStackRegister(name="Python", color="4B8BBE"),
        TechStackRegister(name="Java", color="34495E"),
        TechStackRegister(name="PHP", color="787CB5"),
        TechStackRegister(name="C", color="6e9ad0"),
        TechStackRegister(name="C++", color="6e9ad0"),
        TechStackRegister(name="C#", color="6e9ad0"),
        TechStackRegister(name="Crystal", color="black"),
        TechStackRegister(name="Dart", color="0075BA"),
        TechStackRegister(name="Elixir", color="433A61"),
        TechStackRegister(name="Erlang", color="BE242C"),
        TechStackRegister(name="Fortran", color="B07056"),
        TechStackRegister(name="Go", color="29BEB0"),
        TechStackRegister(name="JavaScript", color="F0DB4F"),
        TechStackRegister(name="TypeScript", color="009FDF"),
        TechStackRegister(name="Kotlin", color="2855D0"),
        TechStackRegister(name="R", color="276DC2"),
        TechStackRegister(name="Ruby", color="D51F06"),
        TechStackRegister(name="Rust", color="B7410E"),
        TechStackRegister(name="Vue", color="41B883"),
        TechStackRegister(name="React", color="4CCCD9"),
        TechStackRegister(name="Svelte", color="F95701"),
        TechStackRegister(name="NodeJS", color="68A063"),
    ]


def get_frameworks() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Framework"), [
        TechStackRegister(name="Django", color="193e2f"),
        TechStackRegister(name="FastAPI", color="329688"),
        TechStackRegister(name="Flask", color="000000"),
        TechStackRegister(name="Sanic", color="4449c8"),
        TechStackRegister(name="Spring", color="76b44d"),
        TechStackRegister(name="SpringBoot", color="76b44d"),
        TechStackRegister(name="Gin", color="338fce"),
        TechStackRegister(name="AngularJS", color="d9283c"),
        TechStackRegister(name="Bootstrap", color="841af6"),
        TechStackRegister(name="DjangoRestFramework", color="792d2e"),
        TechStackRegister(name="Ember", color="d84a36"),
        TechStackRegister(name="Flutter", color="63d1fb"),
        TechStackRegister(name="Codeigniter", color="cd451e"),
        TechStackRegister(name="Laravel", color="e43a32"),
    ]


def get_databases() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Database"), [
        TechStackRegister(name="MySQL", color="206188"),
        TechStackRegister(name="MariaDB", color="0c2c62"),
        TechStackRegister(name="Redis", color="ce2b26"),
        TechStackRegister(name="MongoDB", color="39a554"),
        TechStackRegister(name="OracleDB", color="e21929"),
        TechStackRegister(name="MsSQL", color="231f20"),
        TechStackRegister(name="Cubrid", color="231f20"),
    ]


def get_infraes() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Infra"), [
        TechStackRegister(name="Docker", color="4092e2"),
        TechStackRegister(name="Kubernetes", color="3e6ada"),
        TechStackRegister(name="Nginx", color="2e913f"),
        TechStackRegister(name="Apache Http Server", color="c01f29"),
        TechStackRegister(name="NHN Cloud", color="2a5bda"),
        TechStackRegister(name="AWS", color="e79231"),
        TechStackRegister(name="Azure", color="41b6e7"),
        TechStackRegister(name="CloudFlare", color="e37c2e"),
        TechStackRegister(name="Terraform", color="5f3cd8"),
        TechStackRegister(name="Prometheus", color="d54e31"),
        TechStackRegister(name="Fluentd", color="385f9e"),
        TechStackRegister(name="Grafana", color="dd582f"),
        TechStackRegister(name="SysDig", color="3aa6bf"),
        TechStackRegister(name="Jenkins", color="000000"),
        TechStackRegister(name="TravisCI", color="c2324a"),
        TechStackRegister(name="GitHub Action", color="3e89fa"),
    ]


def get_mldl() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="ML/DL"), [
        TechStackRegister(name="Keras", color="bf000c"),
        TechStackRegister(name="PyTorch", color="dc543d"),
        TechStackRegister(name="Tensorflow", color="ee8a24"),
    ]


def get_others() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Others"), [
        TechStackRegister(name="GitHub", color="212121"),
        TechStackRegister(name="GitLab", color="d0402d"),
        TechStackRegister(name="SVN", color="8097c1"),
        TechStackRegister(name="Jira", color="3e81f2"),
        TechStackRegister(name="Confluence", color="275cca"),
        TechStackRegister(name="Slack", color="000000"),
        TechStackRegister(name="Dooray", color="2a5bda"),
        TechStackRegister(name="Notion", color="000000"),
        TechStackRegister(name="OpenAPI", color="8de346"),
        TechStackRegister(name="Swagger", color="8de346"),
        TechStackRegister(name="PostMan", color="eb683b"),
    ]


command = CreateTechCommand(argparse.ArgumentParser())
command.operate()
