from fastapi import APIRouter, status
from pydantic import Field

from src.common.base_model import BaseModel
from src.core.store.store_repo import IStoreRepo, StoreRepo
from src.core.voucher.entities import Voucher
from src.core.voucher.use_case import get_by_id_or_slug
from src.delivery.http.http_exceptions import NotFoundHttpException
from src.delivery.http.router_helper import authenticated_route, Request, IMAGE_BASE_URL
from src.delivery.http.routers.common.responses import (
    ListResponseMeta,
    VoucherResponseObject,
)
from src.delivery.http.routers.store_router import StoreResponseObject

router = APIRouter(prefix="/coupons")

VOUCHER_IMAGE_URL = f"{IMAGE_BASE_URL}/coupon/coupon_image"


class VoucherResponse(BaseModel):
    data: VoucherResponseObject
    included: list[StoreResponseObject]
    meta: ListResponseMeta = Field(
        default_factory=ListResponseMeta, description="Contains meta data like order"
    )

    @classmethod
    def create_from_voucher(
        cls, voucher: Voucher, store_repo: IStoreRepo = StoreRepo()
    ) -> "VoucherResponse":
        # TODO: we shouldn't be using repo in router layer. Fix this
        stores = store_repo.get_by_ids([voucher.store_id])
        return cls.model_validate(
            {
                "data": VoucherResponseObject.create_from_voucher(voucher),
                "included": [
                    StoreResponseObject.create_from_store(store) for store in stores
                ],
                "meta": {"order": [voucher.id]},
            }
        )


@router.get("/{id_or_slug}", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def get_voucher(id_or_slug: str, request: Request) -> VoucherResponse:
    voucher = get_by_id_or_slug(id_or_slug, request)
    if not voucher:
        raise NotFoundHttpException(
            detail=f"Voucher not found with id/slug: {id_or_slug}"
        )
    else:
        return VoucherResponse.create_from_voucher(voucher)
