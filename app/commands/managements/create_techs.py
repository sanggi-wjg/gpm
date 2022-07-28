import argparse
import os
import sys
from typing import List, Tuple

sys.path.append(os.path.abspath('.'))

from app.service import tech_service
from app.service.tech_service import find_or_create_tech_category_by_name
from app.schemas.tech_schema import TechCategoryRegister, TechStackRegister
from app.commands.managements.base_command import BaseCommand


class CreateTechCommand(BaseCommand):
    help: str = "Create tech categories and stacks"

    def add_arguments(self):
        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        tech_category_register, tech_stack_registers = get_programming_languages()
        self.create_techs(tech_category_register, tech_stack_registers)

        tech_category_register, tech_stack_registers = get_frameworks()
        self.create_techs(tech_category_register, tech_stack_registers)

        tech_category_register, tech_stack_registers = get_databases()
        self.create_techs(tech_category_register, tech_stack_registers)

    def create_techs(self, tech_category_register: TechCategoryRegister, tech_stack_registers: List[TechStackRegister]):
        tech_category = find_or_create_tech_category_by_name(self.db, tech_category_register)
        self.info(f"Create {tech_category.name} or not")

        for tech_stack in tech_stack_registers:
            tech_service.create_tech_stack(self.db, tech_category.id, tech_stack)
            self.debug(f"Create {tech_stack.name} or not")


def get_programming_languages() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Programming Language"), [
        TechStackRegister(name="Python"),
        TechStackRegister(name="Java"),
        TechStackRegister(name="PHP"),
        TechStackRegister(name="C"),
        TechStackRegister(name="C++"),
        TechStackRegister(name="C#"),
        TechStackRegister(name="C#"),
        TechStackRegister(name="Crystal"),
        TechStackRegister(name="Dart"),
        TechStackRegister(name="Elixir"),
        TechStackRegister(name="Erlang"),
        TechStackRegister(name="Fortran"),
        TechStackRegister(name="Go"),
        TechStackRegister(name="JavaScript"),
        TechStackRegister(name="TypeScript"),
        TechStackRegister(name="Kotlin"),
        TechStackRegister(name="R"),
        TechStackRegister(name="Ruby"),
        TechStackRegister(name="Rust"),
        TechStackRegister(name="Vue"),
        TechStackRegister(name="React"),
        TechStackRegister(name="Svelte"),
    ]


def get_frameworks() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Framework"), [
        TechStackRegister(name="Django"),
        TechStackRegister(name="FastAPI"),
        TechStackRegister(name="Flask"),
        TechStackRegister(name="Sanic"),
        TechStackRegister(name="Spring"),
        TechStackRegister(name="SpringBoot"),
        TechStackRegister(name="Gin"),
        TechStackRegister(name="Angular"),
        TechStackRegister(name="Bootstrap"),
        TechStackRegister(name="DjangoRestFramework"),
        TechStackRegister(name="Ember"),
        TechStackRegister(name="Flutter"),
        TechStackRegister(name="Codeigniter"),
        TechStackRegister(name="Laravel"),
    ]


def get_databases() -> Tuple[TechCategoryRegister, List[TechStackRegister]]:
    return TechCategoryRegister(name="Database"), [
        TechStackRegister(name="MySQL"),
        TechStackRegister(name="MariaDB"),
        TechStackRegister(name="Redis"),
        TechStackRegister(name="MongoDB"),
        TechStackRegister(name="OracleDB"),
        TechStackRegister(name="MsSQL"),
        TechStackRegister(name="Cubrid"),
    ]


# TechCategoryRegister(name="Database"), # , , ,

# TechCategoryRegister(name="Infra"), # Docker, Kubernetes, Nginx, Apache Http Server, NHN Cloud, AWS, Azure
# CloudFlare, Terraform, Prometheus, Fluentd, Grafana, SysDig, Jenkins, TravisCI

# TechCategoryRegister(name="ML/DL"), # Keras, PyTorch, Tensorflow

# TechCategoryRegister(name="Others"), # Github, Gitlab, SVN, Jira, Confluence, Slack, Dooray, Notion, OpenAPI


command = CreateTechCommand(argparse.ArgumentParser())
command.operate()
