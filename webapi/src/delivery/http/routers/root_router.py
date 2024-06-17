from fastapi import APIRouter, Request

from src.core.common.context import Context
from src.delivery.http.router_helper import authenticated_route

router = APIRouter()


@router.get("/healthcheck")
def healthcheck():
    return {"status": "healthy"}
