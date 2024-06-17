from fastapi import APIRouter
from fastapi import status
from pydantic import model_validator

from src.common.base_model import BaseModel
from src.core.common.elastic_search.search_elastic_processor_base import (
    ElasticSearchRequest,
)
from src.core.voucher.entities import ElasticSearchVoucher
from src.core.voucher.use_case import (
    elastic_search_vouchers,
)
from src.delivery.http.router_helper import authenticated_route, Request

router = APIRouter()


class SearchVouchersResponse(BaseModel):
    data: list[ElasticSearchVoucher]
    # TODO: counts is actually total count, not derived from data, since we support pagination.
    counts: dict[str, int]

    @model_validator(mode="before")
    @classmethod
    def _set_counts(cls, data: any) -> any:
        """Set counts based on the number of data responses"""
        data["counts"] = {"voucher": len(data["data"])}
        return data


@router.post("/voucher", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def search_vouchers(body: ElasticSearchRequest, request: Request):
    vouchers = elastic_search_vouchers(request=body, context=request.context)

    return SearchVouchersResponse(data=vouchers)
