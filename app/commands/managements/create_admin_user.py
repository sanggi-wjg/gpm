import argparse
import os
import sys

sys.path.append(os.path.abspath('.'))

from app.commands.managements.base_command import BaseCommand
from app.schemas.user_schema import UserRegister
from app.service import user_service


class CreateAdminUserCommand(BaseCommand):
    help: str = "Create Admin User\n Must enter arguments\n eg. -email jayg@nhn-commerce.com -password passw0rd"

    def add_arguments(self):
        self.parser.add_argument('-email', type=str, required=True, help='User Email')
        self.parser.add_argument('-password', type=str, required=True, help='Password')
        self.args = self.parser.parse_args()

    def handle(self, *args, **kwargs):
        user_register = UserRegister(
            email=self.args.email,
            password1=self.args.password,
            password2=self.args.password
        )
        user_service.create_admin_user(self.db, user_register)
        self.debug(f"new_user({user_register.email}) created")


command = CreateAdminUserCommand(argparse.ArgumentParser())
command.operate()
