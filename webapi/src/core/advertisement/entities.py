from enum import StrEnum

from pydantic import Field, HttpUrl

from src.common.base_model import BaseModel

from src.core.common.field_types import UtcDatetime


class AdvertisementStateEnum(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    EXPIRE = "expired"


class Advertisement(BaseModel):
    # Currently these feilds are None if in the database schema they are nullable
    id: str
    slug: str = Field(default=None, description="Slug of advertisement")
    name: str | None = Field(default=None, description="Name of advertisement")
    location: str | None = Field(
        default=None,
        description="Location of advertisement",
        examples=["top", "middle"],
    )
    state: AdvertisementStateEnum | None = Field(
        default=None, description="State of advertisement"
    )
    size: str | None = Field(default=None, description="Size of advertisement")
    start_date: UtcDatetime | None = Field(
        default=None, description="Start date of advertisement"
    )
    end_date: UtcDatetime | None = Field(
        default=None, description="End date of advertisement"
    )
    target: str | None = Field(default=None, description="Target of advertisement")
    url: str | None = Field(
        default=None,
        description="Url of advertisement",
        examples=["https://www2.littlebirdie.com.au/collections/nike-sale"],
    )
    image: str | None = Field(
        default=None, description="Image name of advertisement", examples=["image.png"]
    )

    mobile_image: str | None = Field(
        default=None,
        description="Mobile image name of advertisement",
        examples=["mobile_image.png"],
    )

    external_image_url: str | None = Field(
        default=None,
        description="External image url of advertisement",
        examples=["https://www.nike.com/image.png"],
    )
