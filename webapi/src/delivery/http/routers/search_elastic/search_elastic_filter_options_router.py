from fastapi import APIRouter
from fastapi import status

from src.core.offer.use_case import get_offer_filter_options
from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    FilterOptionsIdEnum,
)
from src.common.base_model import BaseModel
from src.core.sale_event.use_case import get_sale_event_filter_options
from src.core.voucher.use_case import (
    get_voucher_filter_options,
)
from src.core.voucher.voucher_repo import FilterOption

router = APIRouter()


class GetFilterOption(BaseModel):
    key: str
    doc_count: int


class GetFilterOptionsResponseBody(BaseModel):
    options: list[FilterOption]


@router.post("/filter_options", status_code=status.HTTP_200_OK)
def get_filter_options(
    body: ElasticSearchFilterOptionsRequest,
) -> GetFilterOptionsResponseBody:
    if body.id is FilterOptionsIdEnum.VOUCHER_SEARCH:
        return GetFilterOptionsResponseBody(options=get_voucher_filter_options(body))
    elif body.id is FilterOptionsIdEnum.SALE_EVENT_SEARCH:
        return GetFilterOptionsResponseBody(options=get_sale_event_filter_options(body))
    elif body.id is FilterOptionsIdEnum.OFFER_SEARCH_V2:
        return GetFilterOptionsResponseBody(options=get_offer_filter_options(body))

    raise Exception(
        f"Should not reach this line of code. Id: {body.id}, currently not supported"
    )
