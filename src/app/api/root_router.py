from fastapi import APIRouter, FastAPI

from src.app.api.walk_orders import walk_order_router

root_router = APIRouter()
root_router.include_router(
    walk_order_router,
    prefix="/walk_orders",
)


def init_routers(app: FastAPI):
    app.include_router(root_router)
