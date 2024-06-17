from fastapi import APIRouter
from fastapi import status
from pydantic import Field

from src.common.base_model import BaseModel
from src.core.affinity.entities import ElasticSearchUserAffinity
from src.core.affinity.use_case import (
    elastic_search_affinity,
    SearchElasticAffinityRequest,
)
from src.delivery.http.router_helper import authenticated_route, Request

router = APIRouter()


class SearchElasticAffinityResponse(BaseModel):
    data: list[ElasticSearchUserAffinity] | None = Field(
        default=[], description="Affinity details for the user requested"
    )


@router.post("/affinities", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def search_affinity(
    body: SearchElasticAffinityRequest, request: Request
) -> SearchElasticAffinityResponse:
    affinity_details = elastic_search_affinity(request=body, context=request.context)
    if affinity_details is None:
        return SearchElasticAffinityResponse()
    else:
        return SearchElasticAffinityResponse(data=[affinity_details])
