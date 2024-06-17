from fastapi import status, APIRouter
from pydantic import BaseModel, model_validator

from src.core.common.elastic_search.search_elastic_processor_base import (
    ElasticSearchRequest,
)
from src.core.sale_event.entities import ElasticSearchSaleEvent
from src.core.sale_event.use_case import elastic_search_sale_events
from src.delivery.http.router_helper import authenticated_route, Request

router = APIRouter()


class SearchSaleEventsResponse(BaseModel):
    data: list[ElasticSearchSaleEvent]
    # TODO: counts is actually total count, not derived from data, since we support pagination.
    counts: dict[str, int]

    @model_validator(mode="before")
    @classmethod
    def _set_counts(cls, data: any) -> any:
        """Set counts based on the number of data responses"""
        data["counts"] = {"sale_events": len(data["data"])}
        return data


@router.post("/sale_event", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def search_sale_events(
    body: ElasticSearchRequest, request: Request
) -> SearchSaleEventsResponse:
    sale_events = elastic_search_sale_events(request=body, context=request.context)

    return SearchSaleEventsResponse(data=sale_events)
