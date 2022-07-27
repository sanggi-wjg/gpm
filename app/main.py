import logging

import uvicorn
from fastapi import FastAPI

from app.core.config import get_config_settings

from app.database import models
from app.database.database import Engine
from app.exceptions.user_exception import bad_credentials_handler, NotExistEmail, BadCredentials, \
    not_exist_email_handler, user_duplicate_email_handler, DuplicateEmail
from app.routers import home, user, auth

settings = get_config_settings()


def create_app():
    app = FastAPI(
        debug=settings.debug,
        title=settings.app_name,
        description=settings.app_desc,
        contact=dict(name=settings.app_admin_name, ),
    )

    # simple way to create database
    if settings.debug:
        models.Base.metadata.create_all(bind=Engine)
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # exceptions
    app.add_exception_handler(DuplicateEmail, user_duplicate_email_handler)
    app.add_exception_handler(NotExistEmail, not_exist_email_handler)
    app.add_exception_handler(BadCredentials, bad_credentials_handler)

    # routers
    app.include_router(home.router)
    app.include_router(user.router)
    app.include_router(auth.router)

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
