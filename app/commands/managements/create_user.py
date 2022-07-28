import argparse
import os
import sys

sys.path.append(os.path.abspath('.'))

from app.commands.managements.base_command import BaseCommand
from app.schemas.user_schema import UserRegister
from app.service import user_service


class CreateUserCommand(BaseCommand):
    help: str = "Create user"

    def add_arguments(self):
        self.parser.add_argument('-email', type=str, help='User Email', required=True)
        self.parser.add_argument('-password', type=str, help='Password', required=True)
        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        user_register = UserRegister(
            email=self.args.email,
            password1=self.args.password,
            password2=self.args.password
        )

        find_user = user_service.find_user_by_email(self.db, user_register.email)
        if not find_user:
            user_service.create_user(self.db, user_register)
            self.debug(f"new_user({user_register.email}) created")


command = CreateUserCommand(argparse.ArgumentParser())
command.operate()
