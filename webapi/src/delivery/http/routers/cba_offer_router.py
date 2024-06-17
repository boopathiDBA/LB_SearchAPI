from typing import Any, Annotated

from fastapi import status, APIRouter, Header

from src.common.base_model import BaseModel
from src.core.sale_event.use_case import get_unexpired_published_cba_sale_event
from src.core.user.usecase import get_user_wtid
from src.core.voucher.entities import Voucher
from src.core.voucher.use_case import get_unexpired_published_cba_voucher
from src.delivery.http.router_helper import Request, authenticated_route, IMAGE_BASE_URL
from src.delivery.http.routers.common.responses import (
    SaleEventResponseObject,
    VoucherResponseObject,
)

router = APIRouter(prefix="/new_cba_offers")

EXPECTED_CBA_PARAM_VALUE_SIZE = 40


class CbaOffersResponse(BaseModel):
    data: list = []  # default to empty, as might be deprecated but used in front-end
    included: list[SaleEventResponseObject | VoucherResponseObject]


@router.get("", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def get_cba_offers(
    request: Request, wtid: Annotated[str | None, Header()] = None
) -> CbaOffersResponse | list[Any]:
    if (
        len(wtid or "") != EXPECTED_CBA_PARAM_VALUE_SIZE
        or get_user_wtid(request.context.user_id) != wtid
    ):
        return []
    else:
        cba_offers = [
            SaleEventResponseObject.create_from_sale_event(event)
            for event in get_unexpired_published_cba_sale_event()
        ]
        cba_offers += [
            VoucherResponseObject.create_from_voucher(voucher)
            for voucher in get_unexpired_published_cba_voucher()
        ]

        return CbaOffersResponse.model_validate({"included": cba_offers})
