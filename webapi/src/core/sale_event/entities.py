from datetime import datetime

from pydantic import Field, model_validator

from src.common.base_model import Cloner
from src.core.common.base_entity import BaseEntity
from src.core.common.field_types import UtcDatetime


class SaleEventBase(BaseEntity):
    id: str = Field(description="SaleEvent Identifier")
    name: str = Field(description="SaleEvent name", examples=["25% off sitewide"])
    start_at: UtcDatetime = Field(
        description="SaleEvent start_at",
        examples=["2025-07-17T15:50:00.000+0 10:00"],
    )
    expire_at: UtcDatetime | None = Field(
        default=None,
        description="SaleEvent expire_at",
        examples=["2025-07-17T15:50:00.000+0 10:00"],
    )
    published_at: UtcDatetime | None = Field(
        default=None,
        description="SaleEvent published at",
        examples=["2025-07-17T15:50:00.000+0 10:00"],
    )
    slug: str = Field(description="SaleEvent slug", examples=["25-off-sitewide"])
    archived_at: UtcDatetime | None = Field(
        description="SaleEvent archive_at",
        examples=["2025-07-17T15:50:00.000+0 10:00"],
        default=None,
    )
    store_logo: str | None = Field(
        description="SaleEvent store_logo",
        examples=["https://media.littlebirdie.com.au/store/172.jpg"],
        default="",
    )
    # NOTE: Not all SaleEvents have a relation to department, therefore typing is optional None
    department_name: str | None = Field(
        description="SaleEvent department_name", examples=["Fashion"], default=None
    )
    brand_name: str | None = Field(
        description="SaleEvent brand_name", examples=["Nike"], default=None
    )
    # NOTE: Not all SaleEvents have a relation to category, therefore typing is optional None
    category_name: str | None = Field(
        description="SaleEvent category_name", examples=["Nike"], default=None
    )
    store_name: str | None = Field(
        description="SaleEvent store_name", examples=["Appliances Online"], default=None
    )
    sale_event_image: str | None = Field(
        description="sale_event_image can be both type ImageWithUrl & str, based on the API",
        examples=[
            "https://assets.littlebirdie.com.au/uploads/sale_event/sale_event_image/129279/265.png"
        ],
        default=None,
    )
    url: str | None = Field(
        default=None,
        description="SaleEvent url",
        examples=["https://watchdirect.com.au/collections/all-jewellery"],
    )
    offer_text: str | None = Field(default=None, description="SaleEvent offer_text")
    impressions_count: str = Field(
        description="SaleEvent impressions_count", examples=[10]
    )
    fixed_global_score: str = Field(
        description="SaleEvent fixed_global_score", default=""
    )
    type: str | None = None


class ElasticSearchSaleEvent(SaleEventBase):
    """Entity returned from SaleEventRepo.elastic_search(...)"""

    upvoted: bool = False


class ElasticSearchUserAffinitySaleEvent(SaleEventBase):
    pass


class SaleEvent(Cloner[SaleEventBase]):
    # NOTE: These fields are not present in this entity
    # NOTE: Any updates here should also update the SaleEventResponseAttributes
    # in src/delivery/http/routers/common/responses.py, see class for more details why.
    _excluded_fields = ["store_logo", "department_name", "category_name"]

    upvotes_count: int = Field(description=" Sale Event upvotes_count", examples=[0])
    downvotes_count: int = Field(
        description=" Sale Event downvotes_count", examples=[0]
    )
    comments_count: int = Field(description=" Sale Event comments_count", examples=[0])
    click_through_count: int = Field(
        description=" Sale Event click_through_count", examples=[0]
    )
    can_join_sale: bool | None = Field(
        description=" Sale Event can_join_sale", default=None
    )
    # NOTE: This field is set by below model validator
    end_in: str = Field(
        default="No Expire Date",
        description=" Sale Event end_in",
        examples=["Ends 25/06/2025"],
    )
    is_cba_exclusive: bool = Field(description=" Sale Event is_cba_exclusive")

    @model_validator(mode="before")
    @classmethod
    def _maybe_set_end_in(cls, data: any) -> any:
        """Set end_in based on the expire_at if exist"""
        if isinstance(data, dict) and isinstance(data.get("expire_at"), datetime):
            expire_at = data["expire_at"]
            data["end_in"] = f"Ends {expire_at.strftime('%d/%m/%Y')}"
        return data
