from src.core.common.field_types import UtcDatetime
from enum import StrEnum

from pydantic import Field
from src.common.base_model import BaseModel


class FeaturableTypeEnum(StrEnum):
    SALE_EVENT = "SaleEvent"
    VOUCHER = "Coupon"  # Voucher is also known as Coupon
    OFFER = "Deal"  # Offer is also known as Deal
    UNIQUE_COUPON = "UniqueCoupon"
    CUSTOM_LIST = "CustomList"


class TodaysTopPick(BaseModel):
    id: str
    position: int | None = Field(
        description="Position/ranking of featurable", examples=[1, 2, 3, 50]
    )
    listing_url: str | None = Field(
        description="URL of the featurable item",
        examples=[
            "https://littlebirdie.com.au/shop/voucher/up-to-25-off-rrp-sunscreen-sale-1696208609"
        ],
    )
    featurable_id: int | None = Field(description="Id of the featurable item")
    featurable_type: FeaturableTypeEnum | None
    created_at: UtcDatetime = Field(description="Date when the item was created")
    updated_at: UtcDatetime = Field(description="Date when the item was updated")
