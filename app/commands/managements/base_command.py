from argparse import Namespace, ArgumentParser

from sqlalchemy.orm import Session

from app.core.colorful import magenta, green, yellow, red
from app.database.database import command_session_factory


class BaseCommand:
    help: str = ""
    args: Namespace = None

    def __init__(self, parser: ArgumentParser):
        self.debug: callable = magenta
        self.info: callable = green
        self.warning: callable = yellow
        self.error: callable = red
        # self.print.info(f"Command input : {args}")
        # self.args = args
        self.parser: ArgumentParser = parser
        self.db: Session = command_session_factory()
        self.setup()

    def setup(self):
        pass

    def operate(self):
        self.add_arguments()
        self.info(f"START Command: {self.help or None}")
        self.handle()
        self.info("FINISH Command")

    def add_arguments(self):
        raise NotImplementedError("add_arguments must declared")

    def handle(self, *args, **kwargs):
        raise NotImplementedError("operate must declared")
