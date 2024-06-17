from pydantic import Field

from src.core.common.field_types import UtcDatetime
from src.core.common.base_entity import BaseEntity


class Store(BaseEntity):
    """
    Store entity
    """

    id: str = Field(description="Store id")
    slug: str = Field(default=None, description="Slug value of the store")
    name: str | None = Field(default=None, description="Store name")
    upvotes_count: int = Field(default=0, description="Raw count of Up votes")
    downvotes_count: int = Field(default=0, description="Raw count of Down votes")
    followers_count: int = Field(default=0, description="Raw count of followers")
    impressions_count: int = Field(default=0, description="Raw count of impressions")
    comments_count: int = Field(default=0, description="Raw count of Comments")
    deals_count: int = Field(default=0, description="Raw count of Deals")
    coupons_count: int = Field(default=0, description="Raw count of Coupons")
    sale_events_count: int = Field(default=0, description="Raw count of Sale events")
    products_count: int = Field(default=0, description="Raw count of Products")
    show_history: bool = Field(default=False, description="todo")
    grey_retailer: bool = Field(default=False, description="todo")
    custom_description: str | None = Field(
        default=None, description="Description of the Store"
    )
    social_twitter_url: str | None = Field(
        default=None, description="Twitter url of the Store"
    )
    social_instagram_url: str | None = Field(
        default=None, description="Instagram url of the Store"
    )
    social_facebook_url: str | None = Field(
        default=None, description="Facebook url of the Store"
    )
    social_youtube_url: str | None = Field(
        default=None, description="Youtube url of the Store"
    )
    social_tiktok_url: str | None = Field(
        default=None, description="Tiktok url of the Store"
    )
    social_blog_url: str | None = Field(
        default=None, description="Blog url of the Store"
    )
    accepted_payments: list[str] = Field(
        default=[], description="List of payment option strings"
    )
    header_image: str | None = Field(default=None, description="Store header image url")
    followed: bool | None = Field(
        default=None, description="Is the Store followed by the requested user?"
    )
    store_rating: float | None = Field(default=None, description="Store rating")
    store_reviews: int | None = Field(default=None, description="Store reviews count")
    website_url: str | None = Field(default=None, description="Store website")
    logo_url: str | None = Field(default=None, description="Store logo url")


class TopStoreDBEntity(BaseEntity):
    """
    This entity represents Materialized View for Top Stores
    mv_top_stores
    """

    id: str | None = Field(default=None)
    source_id: str | None = Field(default=None)
    name: str | None = Field(default=None)
    deals_count: int | None = Field(default=None)
    refreshed_at: UtcDatetime | None = Field(default=None)
    score: int | None = Field(default=None)
    fixed_global_score: int | None = Field(default=None)
    rank: int | None = Field(default=None)
