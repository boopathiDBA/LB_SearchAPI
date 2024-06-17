from pydantic import Field, model_validator, HttpUrl, FileUrl
from pathlib import Path


from src.core.voucher.entities import Voucher, VoucherTypeEnum
from src.common.base_model import BaseModel, Cloner
from src.core.sale_event.entities import SaleEvent
from src.delivery.http.router_helper import IMAGE_BASE_URL

SALE_EVENT_IMAGE_URL = f"{IMAGE_BASE_URL}/sale_event/sale_event_image"
VOUCHER_IMAGE_URL = f"{IMAGE_BASE_URL}/coupon/coupon_image"
UNIQUE_VOUCHER_IMAGE_URL = f"{IMAGE_BASE_URL}/unique_coupon/coupon_image"


class ImageWithUrl(BaseModel):
    url: HttpUrl | None = Field(
        default=None, description="Image URL for SaleEvent, Coupon, etc"
    )


class Relationship(BaseModel):
    id: str
    type: str


class RelationshipData(BaseModel):
    data: Relationship | None


class Relationships(BaseModel):
    brand: RelationshipData
    category: RelationshipData
    department: RelationshipData
    store: RelationshipData
    user: RelationshipData

    @classmethod
    def _get_relationship_data_object(cls, _type: str, _id: str) -> dict:
        return {"data": {"id": _id, "type": _type} if _id else None}

    @classmethod
    def create_from_ids(
        cls,
        *,
        brand_id: str = None,
        department_id: str = None,
        category_id: str = None,
        store_id: str = None,
        user_id: str = None,
    ) -> "Relationships":
        return cls.model_validate(
            {
                "brand": cls._get_relationship_data_object("brand", brand_id),
                "department": cls._get_relationship_data_object(
                    "department", department_id
                ),
                "category": cls._get_relationship_data_object("category", category_id),
                "store": cls._get_relationship_data_object("store", store_id),
                "user": cls._get_relationship_data_object("user", user_id),
            }
        )


class SaleEventResponseLinks(BaseModel):
    sale_event_url: str
    image_url: HttpUrl

    @classmethod
    def create_from_sale_event(cls, sale_event: SaleEvent) -> "SaleEventResponseLinks":
        return cls.model_validate(
            {
                "sale_event_url": f"/shop/sale-event/{sale_event.slug}",
                "image_url": (
                    f"{SALE_EVENT_IMAGE_URL}/{sale_event.id}/{sale_event.sale_event_image}"
                    if sale_event.sale_event_image is not None
                    else None
                ),
            }
        )


class SaleEventResponseAttributes(Cloner[SaleEvent]):
    # NOTE: this currently requires Cloner to be inherited and _excluded_fields to be defined
    # This seems to be a bug
    _excluded_fields = ["store_logo", "department_name", "category_name"]

    # This overrides the field in parent class to include the URL for the API response
    sale_event_image: ImageWithUrl | None = Field(
        default=None, description="Coupon Image URL"
    )

    @model_validator(mode="before")
    @classmethod
    def _maybe_set_sale_event_image(cls, data: any) -> any:
        """Set sale_event image URL for the API response if exist"""

        if isinstance(data, dict) and (
            sale_event_image_str := data.get("sale_event_image", None)
        ):
            data["sale_event_image"] = ImageWithUrl(
                url=f"{SALE_EVENT_IMAGE_URL}/{data['id']}/{sale_event_image_str}"
            )

        return data


class SaleEventResponseObject(BaseModel):
    id: str
    type: str = "sale_event"
    attributes: SaleEventResponseAttributes
    links: SaleEventResponseLinks

    @classmethod
    def create_from_sale_event(cls, sale_event: SaleEvent) -> "SaleEventResponseObject":
        """Factory method to create sale event response object from sale event"""
        return cls.model_validate(
            {
                "id": sale_event.id,
                "attributes": dict(sale_event),
                "links": SaleEventResponseLinks.create_from_sale_event(sale_event),
            }
        )


class VoucherResponseLinks(BaseModel):
    coupon_url: str
    image_url: HttpUrl
    large_image: str | None
    affiliate_url: str


class VoucherResponseAttributes(Cloner[Voucher]):
    _included_fields = [
        "name",
        "slug",
        "offer",
        "description",
        "limitations",
        "upvotes_count",
        "downvotes_count",
        "comments_count",
        "impressions_count",
        "click_through_count",
        "expired",
        "coupon_code",
        "updated_at_label",
        "created_at_label",
        "published_at_label",
        "updated_at",
        "created_at",
        "availability",
        "discount_percent",
        "discount_amount",
        "coupon_type",
        "claimed_code_count",
        "unclaimed_code_count",
        "running_low_is_met",
        "type",
        "store_name",
        "limit_per_customer",
        "is_cba_exclusive",
        "expire_at",
        "is_cba_icp",
        "available_for_use",
        "coupon_image",  # This will be overridden below
    ]

    # This overrides the coupon_image field to include the URL for the API response
    coupon_image: ImageWithUrl | None = Field(
        default=None, description="Coupon Image URL"
    )

    @model_validator(mode="before")
    @classmethod
    def _maybe_set_coupon_image(cls, data: any) -> any:
        """Set coupon image URL for the API response if exist"""
        if isinstance(data, dict) and (
            coupon_image_str := data.get("coupon_image", None)
        ):
            if data["type"] == VoucherTypeEnum.UNIQUE_COUPON:
                base_image_url = UNIQUE_VOUCHER_IMAGE_URL
            else:
                base_image_url = VOUCHER_IMAGE_URL
            data["coupon_image"] = ImageWithUrl(
                url=f"{base_image_url}/{data['id']}/{coupon_image_str}"
            )

        return data


class VoucherResponseObject(BaseModel):
    id: str
    type: str = "coupon"
    attributes: VoucherResponseAttributes
    links: VoucherResponseLinks
    relationships: Relationships

    @classmethod
    def create_from_voucher(cls, voucher: Voucher) -> "VoucherResponseObject":
        return cls.model_validate(
            {
                "id": voucher.id,
                # Use contruct over model_validate to avoid running validators again.
                "attributes": VoucherResponseAttributes.model_validate(
                    voucher.model_dump()
                ),
                "links": {
                    "coupon_url": f"/shop/voucher/{voucher.slug}",
                    "image_url": f"{VOUCHER_IMAGE_URL}/{voucher.id}/{voucher.coupon_image}",
                    "large_image": voucher.large_image,
                    "affiliate_url": f"/goto/coupon/{voucher.slug}",
                },
                "relationships": Relationships.create_from_ids(
                    brand_id=voucher.brand_id,
                    department_id=voucher.department_id,
                    category_id=voucher.category_id,
                    store_id=voucher.store_id,
                    user_id=voucher.user_id,
                ),
            }
        )


class ListResponseMeta(BaseModel):
    order: list[int] = Field(default=[], description="List of ids in order to be shown")
