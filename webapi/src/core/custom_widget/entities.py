from enum import StrEnum

from pydantic import Field

from src.common.base_model import Cloner
from src.core.common.base_entity import BaseEntity


class CustomWidgetPositionEnum(StrEnum):
    HERO = "hero"
    TOP = "top"
    TOP_MIDDLE = "top-middle"
    BOTTOM = "bottom"
    CMS = "cms"


class CustomWidgetItemTypeEnum(StrEnum):
    SALE_EVENT = "SaleEvent"
    VOUCHER = "Coupon"  # Voucher is also known as Coupon
    OFFER = "Deal"  # Offer is also known as Deal


class CustomWidgetStateEnum(StrEnum):
    PUBLISHED = "published"
    ARCHIVED = "archived"
    REJECTED = "rejected"
    UNPUBLISHED = "unpublished"
    PENDING = "pending"


class CustomWidgetDBEntity(BaseEntity):
    """
    Structure of the DB table
    """

    id: str = Field(description="CustomWidgetItem identifier ", examples=["6"])
    bg_color: str | None = Field(
        default=None, description="CustomWidgetItem identifier ", examples=["#393939"]
    )
    position: CustomWidgetPositionEnum = Field(
        description="CustomWidgetItem identifier ", examples=["hero"]
    )
    slug: str = Field(
        description="CustomWidgetItem identifier ",
        examples=["9e28259e-cac3-476b-a758-8f9655c96132"],
    )
    state: CustomWidgetStateEnum = Field(
        description="CustomWidgetItem identifier ", examples=["published"]
    )
    title: str = Field(
        description="CustomWidgetItem identifier ", examples=["Some Testing "]
    )
    description: str = Field(
        description="CustomWidgetItem identifier ",
        examples=["This is the description of toms test"],
    )
    view_more_link: str | None = Field(
        default=None,
        description="CustomWidgetItem identifier ",
        examples=["https://www.littlebirdie.com.au/search/Dyson%20Australia"],
    )


class CustomWidgetItem(BaseEntity):
    """
    Structure of the DB table
    """

    id: str = Field(description="CustomWidgetItem identifier ")
    item_id: str = Field(description="CustomWidgetItem type identifier")
    item_type: CustomWidgetItemTypeEnum = Field(description="CustomWidgetItem type")
    type: str = Field(description="default type value", default="custom_widget_item")
    position: int = Field(description="position of item", examples=[1, 2])
    listing_url: str | None = Field(default=None, description="listing_url of item")
    sponsored: bool = Field(description="boolean flag of item")


class CustomWidget(CustomWidgetDBEntity):
    items: list[CustomWidgetItem]
