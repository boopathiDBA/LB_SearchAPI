from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr, model_validator, Field

from src.core.braze.usecase import (
    get_users_by_email,
    get_users_by_external_ids,
    merge_users_by_external_ids,
)
from src.core.braze.braze_repo import BrazeMergeUsersRequest
from src.core.braze.entities import BrazeUser


router = APIRouter(prefix="/braze")


class GetBrazeUsersRequest(BaseModel):
    external_ids: list[str] | None = Field(default=None, description="Braze user id")
    email_address: EmailStr | None = Field(default=None, description="Braze user email")

    @model_validator(mode="after")
    def _check_email_or_externalids(self):
        if not self.email_address and not self.external_ids:
            raise ValueError("Either external_ids or email_address required")
        return self


class BrazeMergeUsersResponse(BaseModel):
    message: str = Field(description="Merge status")


class GetBrazeUsersResponse(BaseModel):
    data: list[BrazeUser]


@router.post("/users/merge", status_code=status.HTTP_200_OK)
def merge_braze_users(user_data: BrazeMergeUsersRequest) -> BrazeMergeUsersResponse:
    merge_status = merge_users_by_external_ids(merge_request=user_data)

    return BrazeMergeUsersResponse(message=merge_status)


@router.post("/users", status_code=status.HTTP_200_OK)
def get_braze_users(user_data: GetBrazeUsersRequest) -> GetBrazeUsersResponse:
    if user_data.external_ids:
        braze_users = get_users_by_external_ids(user_data.external_ids)
    else:
        braze_users = get_users_by_email(user_data.email_address)

    return GetBrazeUsersResponse(data=braze_users)
