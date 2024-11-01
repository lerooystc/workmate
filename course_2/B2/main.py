from api.base import api_router
from db.session import lifespan
from fastapi import FastAPI


def include_router(app: FastAPI):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title="Parser", version="1.2", lifespan=lifespan)
    include_router(app)
    return app


app = start_application()
