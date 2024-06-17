from fastapi import APIRouter, status
from pydantic import Field, field_validator, model_validator, HttpUrl
from pydantic.fields import FieldInfo

from src.common.base_model import BaseModel, Cloner
from src.common.string_utils import pretty_count
from src.core.brand.entities import Brand
from src.core.brand.use_case import (
    get_brand_by_friendly_id,
    get_brands_followed_by_user_id,
)
from src.core.common.repository import FriendlyId
from src.delivery.http.http_exceptions import NotFoundHttpException
from src.delivery.http.router_helper import Request, authenticated_route

router = APIRouter(prefix="/brands")


class BrandAttributes(Cloner[Brand]):
    _included_fields = ["name", "slug", "followed"]

    followers_count: str = FieldInfo.merge_field_infos(
        Brand.model_fields.get("followers_count")
    )
    products_count: str = FieldInfo.merge_field_infos(
        Brand.model_fields.get("products_count")
    )
    deals_count: str = FieldInfo.merge_field_infos(
        Brand.model_fields.get("deals_count")
    )
    coupons_count: str = FieldInfo.merge_field_infos(
        Brand.model_fields.get("coupons_count")
    )
    sale_events_count: str = FieldInfo.merge_field_infos(
        Brand.model_fields.get("sale_events_count")
    )

    @field_validator(
        "followers_count",
        "products_count",
        "deals_count",
        "coupons_count",
        "sale_events_count",
    )
    @classmethod
    def _format_pretty_count(cls, count: str) -> str:
        """Format int into pretty count format"""
        return pretty_count(int(count)) if count else "0"


class BrandLinks(Cloner[Brand]):
    _included_fields = ["logo_url"]

    brand_url: str = Field(description="Url in the format /shop/brand/{slug}")

    @classmethod
    def create_from_brand(cls, brand: Brand) -> "BrandLinks":
        return cls.model_validate(
            {**dict(brand), "brand_url": f"/shop/brand/{brand.slug}"}
        )


class BrandResponseObject(BaseModel):
    attributes: BrandAttributes = Field(default=None, description="Brand attributes")
    id: str = Field(description="Brand id")
    type: str = Field(default="brand", description="Type of the object")
    links: BrandLinks = Field(description="Brand links like brand url, logo url")

    @classmethod
    def create_from_brand(cls, brand: Brand) -> "BrandResponseObject":
        """Factory method to create brand response object from brand"""
        brand_dict = brand.model_dump()
        return cls.model_validate(
            {
                "attributes": brand_dict,
                "id": brand.id,
                "links": BrandLinks.create_from_brand(brand),
            }
        )


class BrandResponse(BaseModel):
    data: BrandResponseObject = Field(description="Brand object")

    @classmethod
    def create_from_brand(cls, brand: Brand) -> "BrandResponse":
        """Factory method to create brand response object from brand"""
        return cls.model_validate(
            {"data": BrandResponseObject.create_from_brand(brand)}
        )


class BrandListMeta(BaseModel):
    order: list[int] = Field(
        default=[], description="List of brand ids in order to be shown"
    )


class BrandListResponse(BaseModel):
    data: list[BrandResponseObject] = Field(default=[], description="List of brands")
    meta: BrandListMeta = Field(
        default_factory=BrandListMeta, description="Contains meta data like order"
    )

    @classmethod
    def create_from_brands(cls, brands: list[Brand]) -> "BrandListResponse":
        """Factory method to create brand response object from brand"""
        return cls.model_validate(
            {
                "data": [
                    BrandResponseObject.create_from_brand(brand) for brand in brands
                ],
                "meta": {"order": [int(brand.id) for brand in brands]},
            }
        )


@router.get("/{friendly_id}", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def get_brand(friendly_id: FriendlyId, request: Request) -> BrandResponse:
    brand = get_brand_by_friendly_id(friendly_id, request.context)

    if brand:
        return BrandResponse.create_from_brand(brand)
    else:
        raise NotFoundHttpException(
            detail=f"Brand not found with friendly id/slug: {friendly_id}"
        )


@router.get("", status_code=status.HTTP_200_OK)
def get_brands_followed_by(followed_by: str) -> BrandListResponse:
    brands = get_brands_followed_by_user_id(followed_by)
    return BrandListResponse.create_from_brands(brands)
