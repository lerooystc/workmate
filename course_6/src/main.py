from src.api.base import api_router
from src.config import settings
from src.db.session import lifespan
from src.common.middleware import RouterCacheControlResetMiddleware
from fastapi import FastAPI


def include_router(app: FastAPI):
    app.include_router(api_router)


def start_application():
    app = FastAPI(
        title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan
    )
    app.add_middleware(RouterCacheControlResetMiddleware)
    include_router(app)
    return app


app = start_application()
