from enum import StrEnum
from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field, HttpUrl

from src.delivery.http.router_helper import IMAGE_BASE_URL
from src.common.base_model import BaseModel
from src.core.advertisement.entities import Advertisement
from src.core.advertisement.use_case import get_advertisements
from src.core.common.repository import FriendlyId

ADVERTISEMENT_IMAGE_URL = f"{IMAGE_BASE_URL}/posts"

router = APIRouter(prefix="/marketing")


class GetMarketingAdvertsResponseDataLinksUrl(BaseModel):
    url: HttpUrl = ""


class ImageTypeEnum(StrEnum):
    """Used to determine url path"""

    STANDARD = "image"
    MOBILE = "mobile_image"


class GetMarketingAdvertsResponseDataLinksImage(BaseModel):
    url: HttpUrl
    mini: GetMarketingAdvertsResponseDataLinksUrl = Field(description="Mini image url")
    thumb: GetMarketingAdvertsResponseDataLinksUrl = Field(
        description="Thumbnail image url"
    )
    medium: GetMarketingAdvertsResponseDataLinksUrl = Field(
        description="Medium image url"
    )

    @classmethod
    def maybe_create_from_image_name(
        cls,
        *,
        advertisement: Advertisement,
        image_name: str | None,
        image_type: ImageTypeEnum,
    ) -> "GetMarketingAdvertsResponseDataLinksImage | None":
        """Factory create links url. This currently handles two cases, for when advertisement.image exist
        or when advertisement.image_url exist. The urls differ by the the path `image` and `mobile_image`
        hence an enum ImageTypeEnum was used"""
        if image_name is None:
            return None
        else:
            return cls.model_validate(
                {
                    "url": f"{ADVERTISEMENT_IMAGE_URL}/{image_type}/{advertisement.id}/{image_name}",
                    "mini": {
                        "url": f"{ADVERTISEMENT_IMAGE_URL}/{image_type}/{advertisement.id}/mini_{advertisement.image}"
                    },
                    "thumb": {
                        "url": f"{ADVERTISEMENT_IMAGE_URL}/{image_type}/{advertisement.id}/thumb_{advertisement.image}"
                    },
                    "medium": {
                        "url": f"{ADVERTISEMENT_IMAGE_URL}/{image_type}/{advertisement.id}/medium_{advertisement.image}"
                    },
                }
            )


class GetMarketingAdvertsResponseDataLinks(BaseModel):
    url: str
    image: GetMarketingAdvertsResponseDataLinksImage | None = Field(
        default=None, description="Web image urls"
    )

    mobile_image: GetMarketingAdvertsResponseDataLinksImage | None = Field(
        default=None, description="Mobile image urls"
    )

    external_image_url: HttpUrl | None = Field(
        default=None, description="External image url"
    )

    affiliate_url: str

    @classmethod
    def create_from_advertisement(
        cls,
        advertisement: Advertisement,
    ) -> "GetMarketingAdvertsResponseDataLinks":
        """Factory create method to create object from advertisement."""
        return cls.model_validate(
            {
                "url": advertisement.url,
                "image": GetMarketingAdvertsResponseDataLinksImage.maybe_create_from_image_name(
                    advertisement=advertisement,
                    image_name=advertisement.image,
                    image_type=ImageTypeEnum.STANDARD,
                ),
                "mobile_image": GetMarketingAdvertsResponseDataLinksImage.maybe_create_from_image_name(
                    advertisement=advertisement,
                    image_name=advertisement.mobile_image,
                    image_type=ImageTypeEnum.MOBILE,
                ),
                "external_image_url": advertisement.external_image_url,
                "affiliate_url": f"/goto/advertisement/{advertisement.slug}",
            }
        )


class GetMarketingAdvertsResponseData(BaseModel):
    id: str
    type: str = "advertisement"
    attributes: Advertisement
    links: GetMarketingAdvertsResponseDataLinks


class GetMarketingAdvertsMeta(BaseModel):
    order: list[int]


class GetMarketingAdvertsResponse(BaseModel):
    data: list[GetMarketingAdvertsResponseData]
    meta: GetMarketingAdvertsMeta

    @classmethod
    def create_from_advertisements(
        cls,
        advertisements: list[Advertisement],
    ) -> "GetMarketingAdvertsResponse":
        """Factory create method to create object from a list of advertisements."""
        return cls.model_validate(
            {
                "data": [
                    {
                        "id": advertisement.id,
                        "attributes": advertisement,
                        "links": GetMarketingAdvertsResponseDataLinks.create_from_advertisement(
                            advertisement
                        ),
                    }
                    for advertisement in advertisements
                ],
                "meta": {
                    "order": [int(advertisement.id) for advertisement in advertisements]
                },
            }
        )


@router.get("/adverts")
def get_marketing_adverts(
    by_page: Annotated[
        str | None,
        Query(
            description="Page to filter by",
            examples=["ranking", "listing"],
        ),
    ] = None,
    by_position: Annotated[
        str | None,
        Query(
            description="Position to filter by",
            examples=["top", "top-middle", "hero", "middle"],
        ),
    ] = None,
    by_list: Annotated[
        str | None,
        Query(
            description="List to filter by",
            examples=[
                "top-deals",
                "new-coupons",
                "trending-brands",
                "top-sales-events",
                "top-price-drops",
                "new-price-drops",
                "new-deals",
                "top-spotters",
                "top-upcoming-sales",
                "top-current-sales",
                "top-coupons",
                "new-sales-events",
                "trending-stores",
            ],
        ),
    ] = None,
    by_department: Annotated[
        FriendlyId | None,
        Query(
            description="Department id or slug to filter by",
            examples=["fashion", "home-kitchen", "health-beauty"],
        ),
    ] = None,
    by_category: Annotated[
        FriendlyId | None,
        Query(
            description="Category id or slug to filter by",
            examples=["eye-care", "custumes", "furniture"],
        ),
    ] = None,
) -> GetMarketingAdvertsResponse:
    advertisements = get_advertisements(
        by_page=by_page,
        by_position=by_position,
        by_list=by_list,
        by_department=by_department,
        by_category=by_category,
    )

    return GetMarketingAdvertsResponse.create_from_advertisements(advertisements)
