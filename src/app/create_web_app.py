from fastapi import FastAPI

from src.app.api.root_router import init_routers
from src.app.depends import init_dependencies


def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    init_dependencies(app)
    return app
