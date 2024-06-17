from datetime import datetime
from enum import StrEnum

from pydantic import Field, model_validator

from src.common.base_model import Cloner
from src.common.datetime_utils import distance_of_time_in_words
from src.common.string_utils import number_to_currency
from src.core.common.base_entity import BaseEntity
from src.core.common.field_types import UtcDatetime


# This enum correspond to column 'type' which has value either UniqueCoupon or NULL
class VoucherTypeEnum(StrEnum):
    UNIQUE_COUPON = "UniqueCoupon"


# This enum correspond to column 'coupon_type'
class CouponTypeEnum(StrEnum):
    PERCENTAGE_DISCOUNT = "percentage_discount"
    DOLLAR_DISCOUNT = "dollar_discount"
    FREE_SHIPPING = "free_shipping"
    BONUS_ITEM = "bonus_item"
    OTHER = "other"


class VoucherDBEntity(BaseEntity):
    """Voucher/Coupon entity with all the DB fields"""

    id: str = Field(description="Voucher Identifier")
    source_id: str | None = Field(description="Aladdin id for this voucher/coupon")
    name: str | None = Field(description="Voucher/Coupon name")
    created_at: UtcDatetime = Field(description="Voucher created_at")
    updated_at: UtcDatetime = Field(description="Voucher updated_at")
    upvotes_count: int = Field(default=0)
    downvotes_count: int = Field(default=0)
    slug: str = Field(description="Unique slug of Voucher")
    comments_count: int = Field(default=0)
    source_last_checked_at: UtcDatetime | None = Field()
    impressions_count: int = Field(default=0)
    click_through_count: int = Field(default=0)
    user_id: str | None = Field(description="id of the user that created the Voucher")
    description: str | None = Field(description="Voucher description")
    start_at: UtcDatetime | None = Field()
    expire_at: UtcDatetime | None = Field()
    availability: list[str] | None = Field(
        description="List of availability info",
        examples=["online, in_store, australia"],
    )
    url: str | None = Field(description="Voucher url")
    state: str | None = Field(
        description="Voucher state", examples=["pending", "published", "archived"]
    )
    coupon_type: CouponTypeEnum | None = Field(
        description="Voucher/coupon type",
        examples=["percentage_discount", "free_shipping"],
    )
    # NOTE: this shouldn't be none, however there are some DB rows where it is null
    coupon_code: str | None = Field(
        description="Voucher coupon code", examples=["LOVE2024"]
    )
    store_id: str | None = Field()
    category_id: str | None = Field()
    published_at: UtcDatetime | None = Field()
    archived_at: UtcDatetime | None = Field()
    rejected_at: UtcDatetime | None = Field()
    discount_percent: float | None = Field()
    shipping_discount_percent: float | None = Field()
    discount_amount: float | None = Field()
    limitations: str | None = Field(
        description="Describes the limitation of the Voucher"
    )
    creator_type: str | None = Field(
        description="Type of creator. See examples", examples=["affiliated", "fan"]
    )
    brand_id: str | None = Field()
    creator_id: str | None = Field(
        description="Same as user_id, i.e. id of the user who created Voucher"
    )
    coupon_image: str | None = Field(
        description="Voucher image link",
        examples=[
            "https://assets.littlebirdie.com.au/uploads/coupon/coupon_image/129279/265.png"
        ],
    )
    followers_count: int = Field(default=0)
    department_id: str | None = Field()
    discarded_at: UtcDatetime | None = Field()
    type: VoucherTypeEnum | None = Field(description="Type of Voucher")
    limit_per_customer: int | None = Field(default=10)
    running_low_threshold: float | None = Field(default=0.1)
    cba_application_image: str | None = Field()
    is_cba_exclusive: bool | None = Field(default=False)
    large_image: str | None = Field()
    updator_id: str | None = Field(description="user id of who updated the Voucher")
    cba_status: str | None = Field()
    is_cba_icp: bool | None = Field(default=False)
    discount_strength: int | None = Field()
    uniqueness: int | None = Field()
    limitation_score: int | None = Field()
    offer_demand_score: int | None = Field()


class TopVoucherDBEntity(BaseEntity):
    """
    This entity represents Materialized View for Top Coupons
    mv_top_coupons
    """

    id: str | None = Field()
    source_id: str | None = Field()
    name: str | None = Field()
    coupon_type: str | None = Field()
    published_at: UtcDatetime | None = Field()
    brand_id: str | None = Field()
    store_name: str | None = Field()
    store_id: str | None = Field()
    category_name: str | None = Field()
    category_id: str | None = Field()
    department_name: str | None = Field()
    department_id: str | None = Field()
    score: int | None = Field()
    fixed_global_score: int | None = Field()
    fixed_department_score: int | None = Field()
    rank: int | None = Field()
    department_rank: int | None = Field()
    category_rank: int | None = Field()
    refreshed_at: UtcDatetime | None = Field()


class VoucherBase(BaseEntity):
    id: str = Field(description="Voucher Identifier")
    name: str = Field(description="Voucher name", examples=["25% off sitewide"])
    start_at: UtcDatetime | None = Field(
        description="Voucher start_at", examples=["2023-04-18T22:00:38.615+0 10:00]"]
    )
    expire_at: UtcDatetime | None = Field(
        description="Voucher expire_at", examples=["2023-04-18T22:00:38.615+0 10:00]"]
    )
    slug: str = Field(description="Voucher slug", examples=["25-off-sitewide"])
    archived_at: UtcDatetime | None = Field(
        description="Voucher archived_at",
        examples=["2023-04-18T22:00:38.615+0 10:00"],
        default=None,
    )
    # store logo extra
    store_logo: str | None = Field(
        default=None,
        description="Voucher store_logo",
        examples=["https://media.littlebirdie.com.au/store/172.jpg"],
    )
    # department name extra
    department_name: str | None = Field(
        description="Voucher department_name", examples=["Fashion"]
    )
    # brand name extra
    brand_name: str | None = Field(
        description="Voucher brand_name", examples=["Nike"], default=""
    )
    # cat name extra
    category_name: str | None = Field(
        description="Voucher category_name", examples=["Jewellery \u0026 Watches"]
    )
    # store name extra
    store_name: str | None = Field(
        description="Voucher store_name", examples=["Watch Direct"]
    )
    # Can be None in OpenSearch, set typing here to avoid runtime error
    coupon_image: str | None = Field(
        description="coupon_image can be both type ImageWithUrl & str, based on the API",
        examples=[
            "https://assets.littlebirdie.com.au/uploads/coupon/coupon_image/129279/265.png"
        ],
        default=None,
    )
    discount_amount: str | None = Field(
        description="Voucher discount_amount", examples=["20.0"], default=None
    )
    # Can be None in OpenSearch, set typing here to avoid runtime error
    coupon_code: str | None = Field(
        description="Voucher coupon_code", examples=["LOVE2024"], default=None
    )
    coupon_type: str = Field(
        description="Voucher coupon_type", examples=["percentage_discount"]
    )
    url: str = Field(
        description="Voucher url",
        examples=["https://watchdirect.com.au/collections/all-jewellery"],
    )
    impressions_count: int = Field(
        description="Voucher impressions_count", examples=[100]
    )
    is_cba_exclusive: bool = Field(
        description="Voucher is_cba_exclusive", default=False
    )
    # fixed_global_score extra
    fixed_global_score: str = Field(description="Voucher is_cba_exclusive", default="")
    type: str | None = None


class ElasticSearchVoucher(VoucherBase):
    """Entity returned from VoucherRepo.elastic_search(...)"""

    upvoted: bool = False


class ElasticSearchUserAffinityVoucher(VoucherBase):
    pass


class Voucher(Cloner[VoucherDBEntity]):
    offer: str | None = Field(
        description="String generated based on coupon type",
        examples=["25% OFF", "Special offer"],
    )
    expired: bool = Field(description="Is this voucher/coupon expired before now")
    updated_at_label: str = Field(default="")
    created_at_label: str = Field(default="")
    published_at_label: str = Field(default="")

    # Below 3 fields are always set with the same default values
    claimed_code_count: int = Field(default=0)
    unclaimed_code_count: int = Field(default=0)
    running_low_is_met: bool = Field(default=False)

    store_name: str | None = Field(
        description="Voucher store_name", examples=["Watch Direct"]
    )
    available_for_use: bool = Field(default=False)

    @model_validator(mode="before")
    @classmethod
    def _set_offer(cls, data: any) -> any:
        """Set special offer string based on the coupon_type"""
        if isinstance(data, dict):
            if isinstance(data.get("coupon_type"), str):
                try:
                    coupon_type = CouponTypeEnum[data["coupon_type"].upper()]
                    discount_amount = data.get("discount_amount")
                    offer = None
                    if (
                        coupon_type == CouponTypeEnum.PERCENTAGE_DISCOUNT
                        and discount_amount
                        and discount_amount > 0
                    ):
                        offer = f"{int(discount_amount)}% OFF"
                    elif coupon_type == CouponTypeEnum.FREE_SHIPPING:
                        offer = "Free Shipping"
                    elif coupon_type == CouponTypeEnum.BONUS_ITEM:
                        offer = "Free Gift"
                    elif coupon_type == CouponTypeEnum.OTHER:
                        offer = "Special offer"
                    elif (
                        coupon_type == CouponTypeEnum.DOLLAR_DISCOUNT
                        and discount_amount
                        and discount_amount > 0
                    ):
                        offer = f"{number_to_currency(discount_amount)} OFF"

                    if offer:
                        data["offer"] = offer
                except KeyError:
                    pass
        return data

    @model_validator(mode="before")
    @classmethod
    def _set_expired(cls, data: any) -> any:
        """Is the voucher expired?"""
        # Only set if expired is not already set
        if isinstance(data, dict) and data.get("expired") is None:
            data["expired"] = (
                True
                if isinstance(data.get("expire_at"), datetime)
                and data.get("expire_at") < datetime.now()
                else False
            )
        return data

    @model_validator(mode="before")
    @classmethod
    def _set_friendly_date_labels(cls, data: any) -> any:
        """Set friendly time labels"""
        if isinstance(data, dict):
            # Only set if labels are not already set
            if not data.get("updated_at_label") and isinstance(
                data.get("updated_at"), datetime
            ):
                data["updated_at_label"] = distance_of_time_in_words(
                    data.get("updated_at"), datetime.now()
                )
            if not data.get("created_at_label") and isinstance(
                data.get("created_at"), datetime
            ):
                data["created_at_label"] = distance_of_time_in_words(
                    data.get("created_at"), datetime.now()
                )
            if not data.get("published_at_label") and isinstance(
                data.get("published_at"), datetime
            ):
                data["published_at_label"] = distance_of_time_in_words(
                    data.get("published_at"), datetime.now()
                )
        return data

    @model_validator(mode="before")
    @classmethod
    def _set_available_for_use(cls, data: any) -> any:
        """Set friendly time labels"""
        if isinstance(data, dict):
            if (
                # Only set if available_for_use is not already set
                data.get("available_for_use") is None
                and isinstance(data.get("start_at"), datetime)
                and isinstance(data.get("expire_at"), datetime)
            ):
                data["available_for_use"] = (
                    data["start_at"] <= datetime.now() < data["expire_at"]
                )
        return data
