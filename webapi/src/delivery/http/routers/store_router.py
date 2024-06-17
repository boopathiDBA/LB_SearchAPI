from fastapi import APIRouter, status
from pydantic import Field, model_validator, field_validator, HttpUrl
from pydantic.fields import FieldInfo

from src.common.base_model import BaseModel, Cloner
from src.common.string_utils import pretty_count
from src.core.common.repository import FriendlyId
from src.core.store.entities import Store
from src.core.store.use_case import (
    get_store_by_friendly_id,
    get_stores_followed_by_user_id,
)
from src.delivery.http.http_exceptions import NotFoundHttpException
from src.delivery.http.router_helper import Request, authenticated_route

router = APIRouter(prefix="/stores")


class StoreHeaderImageThumb(BaseModel):
    url: str | None = Field(default=None, description="Header image thumb url")


class StoreHeaderImage(BaseModel):
    url: str | None = Field(default=None, description="Header image url")
    thumb: StoreHeaderImageThumb | None = Field(
        default=None, description="Header image thumb object"
    )


class StoreAttributes(Cloner[Store]):
    _exclude_fields = ["id", "website_url", "logo_url"]

    upvotes_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("upvotes_count"), default="0"
    )
    downvotes_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("downvotes_count"), default="0"
    )
    followers_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("followers_count"), default="0"
    )
    impressions_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("impressions_count"), default="0"
    )
    comments_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("comments_count"), default="0"
    )
    deals_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("deals_count"), default="0"
    )
    coupons_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("coupons_count"), default="0"
    )
    sale_events_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("sale_events_count"), default="0"
    )
    products_count: str = FieldInfo.merge_field_infos(
        Store.model_fields.get("products_count"), default="0"
    )

    header_image: StoreHeaderImage | None = Field(
        default=None, description="Header image object"
    )

    store_rating: str | None = FieldInfo.merge_field_infos(
        Store.model_fields.get("store_rating")
    )

    @field_validator(
        "upvotes_count",
        "downvotes_count",
        "followers_count",
        "impressions_count",
        "comments_count",
        "deals_count",
        "coupons_count",
        "sale_events_count",
        "products_count",
    )
    @classmethod
    def _format_pretty_count(cls, count: str) -> str:
        """Format count into pretty count format"""
        return pretty_count(int(count)) if count else "0"

    @field_validator("header_image", mode="before")
    @classmethod
    def _set_header_image(cls, header_image: str) -> StoreHeaderImage:
        return StoreHeaderImage.model_validate(
            {"url": header_image, "thumb": {"url": header_image}}
        )

    @field_validator("store_rating")
    @classmethod
    def _set_store_rating(cls, rating: str | None) -> str | None:
        return str(round(float(rating), 1)) if rating else None


class StoreLinks(Cloner[Store]):
    _included_fields = ["logo_url", "website_url"]

    store_url: str = Field(description="Url in the format /shop/store/{slug}")

    @classmethod
    def create_from_store(cls, store: Store) -> "StoreLinks":
        return cls.model_validate(
            {**dict(store), "store_url": f"/shop/store/{store.slug}"}
        )


class StoreResponseObject(BaseModel):
    attributes: StoreAttributes = Field(default=None, description="Store attributes")
    id: str = Field(description="Store id")
    type: str = Field(default="store", description="Type of the object")
    links: StoreLinks = Field(description="Store links")

    @classmethod
    def create_from_store(cls, store: Store) -> "StoreResponseObject":
        """Factory method to create store response object from store"""
        store_dict = store.model_dump()
        return cls.model_validate(
            {
                "attributes": store_dict,
                "id": store.id,
                "links": StoreLinks.create_from_store(store),
            }
        )


class StoreResponse(BaseModel):
    data: StoreResponseObject = Field(description="Store object")

    @classmethod
    def create_from_store(cls, store: Store) -> "StoreResponse":
        """Factory method to create store response object from store"""
        return cls.model_validate(
            {"data": StoreResponseObject.create_from_store(store)}
        )


class StoreListMeta(BaseModel):
    order: list[int] = Field(
        default=[], description="List of store ids in order to be shown"
    )


class StoreListResponse(BaseModel):
    data: list[StoreResponseObject] = Field(
        default=[], description="List of store objects"
    )
    meta: StoreListMeta = Field(
        default_factory=StoreListMeta, description="Contains meta data like order"
    )

    @classmethod
    def create_from_stores(cls, stores: list[Store]) -> "StoreListResponse":
        """Factory method to create store response object from store list"""
        return cls.model_validate(
            {
                "data": [
                    StoreResponseObject.create_from_store(store) for store in stores
                ],
                "meta": {"order": [int(store.id) for store in stores]},
            }
        )


@router.get("/{friendly_id}", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def get_store(friendly_id: FriendlyId, request: Request) -> StoreResponse:
    store = get_store_by_friendly_id(friendly_id, request.context)

    if store:
        return StoreResponse.create_from_store(store)
    else:
        raise NotFoundHttpException(
            detail=f"Store not found with friendly id/slug: {friendly_id}"
        )


@router.get("", status_code=status.HTTP_200_OK)
def get_stores_followed_by(followed_by: str) -> StoreListResponse:
    stores = get_stores_followed_by_user_id(followed_by)
    return StoreListResponse.create_from_stores(stores)
