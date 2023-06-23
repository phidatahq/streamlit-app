from fastapi import APIRouter

from api.routes.status_routes import status_router
from api.routes.llm_routes import llm_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(status_router)
v1_router.include_router(llm_router)
