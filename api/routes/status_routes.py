from fastapi import APIRouter

from api.routes.endpoints import endpoints
from utils.dttm import current_utc_str

# -*- Create a FastAPI router for health checks
status_router = APIRouter(tags=["status"])


@status_router.get(endpoints.PING)
def status_ping():
    """Ping the API"""

    return {"ping": "pong"}


@status_router.get(endpoints.HEALTH)
def status_health():
    """Check the health of the API"""

    return {
        "status": "success",
        "router": "status",
        "path": endpoints.HEALTH,
        "utc": current_utc_str(),
    }
