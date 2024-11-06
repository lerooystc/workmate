from api.base import api_router
from config import settings
from db.session import lifespan
from fastapi import FastAPI


def include_router(app: FastAPI):
    app.include_router(api_router)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan
    )
    include_router(app)
    return app


app = start_application()
