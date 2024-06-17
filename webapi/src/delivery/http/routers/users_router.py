import os

from fastapi import status, APIRouter
from pydantic import HttpUrl

from src.common.base_model import BaseModel, Cloner
from src.core.user.entities import User
from src.core.user.usecase import get_user_details
from src.delivery.http.http_exceptions import (
    NotFoundHttpException,
    UnauthorizedHttpException,
)
from src.delivery.http.router_helper import authenticated_route, Request, IMAGE_BASE_URL

router = APIRouter(prefix="/users")

USER_IMAGE_URL = f"{IMAGE_BASE_URL}/user/avatar"
DEFAULT_PROFILE_IMAGE = os.getenv(
    "DEFAULT_PROFILE_IMAGE",
    "https://uat.littlebirdie.dev/assets/avatar-ddba12e05258094eb8ed250ba33155806926f1c5f311fd7e9edad4f34a589708.svg",
)


class AvatarUrl(BaseModel):
    url: HttpUrl


class UserLinkAvatar(BaseModel):
    url: HttpUrl
    mini: AvatarUrl
    thumb: AvatarUrl

    @classmethod
    def create_from_user(cls, user: User) -> "UserLinkAvatar":
        if user.avatar:
            user_link_avatar = {
                "url": f"{USER_IMAGE_URL}/{user.id}/{user.avatar}",
                "mini": {"url": f"{USER_IMAGE_URL}/{user.id}/mini_{user.avatar}"},
                "thumb": {"url": f"{USER_IMAGE_URL}/{user.id}/thumb_{user.avatar}"},
            }
        else:
            user_link_avatar = {
                "url": DEFAULT_PROFILE_IMAGE,
                "mini": {"url": DEFAULT_PROFILE_IMAGE},
                "thumb": {"url": DEFAULT_PROFILE_IMAGE},
            }
        return cls(**user_link_avatar)


class UserLinkResponse(BaseModel):
    user_url: str
    avatar: UserLinkAvatar


class UserAttributes(Cloner[User]):
    _included_fields = [
        "email",
        "followers_count",
        "slug",
        "upvotes_count",
        "downvotes_count",
        "username",
        "deals_count",
        "coupons_count",
        "sale_events_count",
        "impressions_count",
        "comments_count",
        "upvoted_count",
        "downvoted_count",
        "public_profile_settings",
        "about_complete",
        "notification_setting",
        "hide_popup",
        "popup_count",
        "notification_status",
        "department_followed",
        "brand_followed",
        "store_followed",
    ]


class UserResponseData(BaseModel):
    id: str
    attributes: UserAttributes
    links: UserLinkResponse
    type: str = "user"


class UserResponse(BaseModel):
    data: UserResponseData


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def get_user(user_id: str, request: Request) -> UserResponse:
    user = get_user_details(user_id)
    if not user:
        raise NotFoundHttpException()
    elif request.context.user_id and user.id != request.context.user_id:
        raise UnauthorizedHttpException()
    elif request.context.user_id or user:
        return UserResponse.model_validate(
            {
                "data": {
                    "id": user_id,
                    "attributes": dict(user),
                    "links": UserLinkResponse.model_validate(
                        {
                            "user_url": f"/spotter/{user.slug}",
                            "avatar": UserLinkAvatar.create_from_user(user),
                        }
                    ),
                }
            }
        )
    else:
        raise Exception("Should not reach here")
