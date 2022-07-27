import os
from functools import lru_cache
from os import path, environ

from pydantic import BaseSettings

base = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


def get_env_filepath() -> str:
    filepath = os.path.join(base, "config", environ.get('CONFIG_ENV', '.env.local'))

    if not os.path.exists(filepath):
        raise Exception(f"Not exist file: {filepath}")

    return filepath


class Settings(BaseSettings):
    base_root = base

    app_name: str = "Github Profile Maker"
    app_desc: str = "👍 GRP(Github Profile Maker) helps create markdown file to be used for ur github profile."
    app_version: str = "0.1.0"
    app_admin_name: str = "Sanggi"

    debug: bool = False
    reload: bool = False
    port: int = 9001

    test_user_email:str = "test@example.com"
    test_user_password:str = "passw0rd"

    host: str
    cors_origins: list
    trust_host: list
    secret_key: str
    access_token_algorithm: str
    access_token_expire_minutes: int

    gzip_minimum_size: int

    database_engine: str
    mysql_user: str
    mysql_password: str
    mysql_host: str
    mysql_port: int
    mysql_db_name: str

    class Config:
        env_file = get_env_filepath()

    @property
    def mysql_dsn(self):
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db_name}"

    @property
    def media_root(self):
        root = os.path.join(self.base_root, "media")
        if not os.path.exists(root):
            os.mkdir(root)
        return root

    @property
    def template_root(self):
        root = os.path.join(self.base_root, "templates")
        if not os.path.exists(root):
            os.mkdir(root)
        return root

    @property
    def static_root(self):
        root = os.path.join(self.base_root, "static")
        if not os.path.exists(root):
            os.mkdir(root)
        return root


@lru_cache()
def get_config_settings():
    return Settings()
