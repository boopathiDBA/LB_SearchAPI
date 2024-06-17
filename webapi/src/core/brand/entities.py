from pydantic import Field

from src.core.common.base_entity import BaseEntity


class Brand(BaseEntity):
    """
    Brand entity
    """

    id: str = Field(description="Brand id")
    name: str | None = Field(default=None, description="Brand name")
    slug: str = Field(description="Slug value of the brand")
    url: str | None = Field(default=None, description="Brand url")
    logo_url: str | None = Field(default=None, description="Brand logo url")
    custom_description: str | None = Field(
        default=None, description="Description of the Brand"
    )
    header_image: str | None = Field(
        default=None, description="Header image of the Brand"
    )

    coupons_count: int = Field(default=0, description="Raw coupons count of the Brand")
    comments_count: int = Field(
        default=0, description="Raw comments count of the Brand"
    )
    deals_count: int = Field(default=0, description="Raw deals count of the Brand")
    downvotes_count: int = Field(
        default=0, description="Raw down votes count of the Brand"
    )
    followers_count: int = Field(
        default=0, description="Raw followers count of the Brand"
    )
    impressions_count: int = Field(
        default=0, description="Raw impressions count of the Brand"
    )
    products_count: int = Field(
        default=0, description="Raw products count of the Brand"
    )
    sale_events_count: int = Field(
        default=0, description="Raw sale events count of the Brand"
    )
    upvotes_count: int = Field(default=0, description="Raw up votes count of the Brand")

    social_blog_url: str | None = Field(
        default=None, description="Blog url of the Brand"
    )
    social_facebook_url: str | None = Field(
        default=None, description="Facebook url of the Brand"
    )
    social_instagram_url: str | None = Field(
        default=None, description="Instagram url of the Brand"
    )
    social_tiktok_url: str | None = Field(
        default=None, description="Tiktok url of the Brand"
    )
    social_twitter_url: str | None = Field(
        default=None, description="Twitter url of the Brand"
    )
    social_youtube_url: str | None = Field(
        default=None, description="Youtube url of the Brand"
    )
    # This is not coming from the Brand table but is added as part of a sql join statement with the follow table
    followed: bool | None = Field(
        default=None, description="Is the Brand followed by the requested user?"
    )
