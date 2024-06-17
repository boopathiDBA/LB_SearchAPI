import os
import logging
import requests
from typing import Protocol
from pydantic import Field
from src.common.base_model import BaseModel

from src.core.braze.entities import BrazeUser


class BrazeExternalId(BaseModel):
    external_id: str = Field(description="Braze user id")


class BrazeIdentifierToKeep(BaseModel):
    identifier_to_merge: BrazeExternalId
    identifier_to_keep: BrazeExternalId


class BrazeMergeUsersRequest(BaseModel):
    merge_updates: list[BrazeIdentifierToKeep]


class IBrazeRepo(Protocol):
    """
    Braze interface
    """

    def get_users_by_email(self, email: str) -> list[BrazeUser]:
        pass

    def get_users_by_external_ids(self, external_ids: list[str]) -> list[BrazeUser]:
        pass

    def merge_users_by_external_ids(self, merge_request: BrazeMergeUsersRequest) -> str:
        pass


class BrazeRepo(IBrazeRepo):

    def __init__(self):
        # https://rest.iad-06.braze.com -> Points to braze host for both dev and prod
        self._braze_host = os.getenv("BRAZE_HOST", "https://rest.iad-06.braze.com")
        self._braze_api_key = os.getenv("BRAZE_API_KEY")
        self._user_fields_to_export = list(BrazeUser.model_fields.keys())

    def _make_api_call(self, method, endpoint, payload):
        headers = {
            "Authorization": f"Bearer {self._braze_api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self._braze_host}/{endpoint}"
        try:
            request_func = getattr(requests, method.lower())
            request = request_func(url, headers=headers, json=payload)
            request.raise_for_status()  # checks for HTTP errors in the response

            response = request.json()
        except requests.RequestException as e:
            # Checkout the possible list of errors from braze:
            # https://www.braze.com/docs/api/endpoints/user_data/post_users_merge/#example-success-response
            # Todo: Uncomment this logger, once logging setup is completed
            # logger.error(f"Request Exception: {e}")
            raise e
        return response

    def get_users_by_email(self, email: str) -> list[BrazeUser]:
        payload = {
            "email_address": email,
            "fields_to_export": self._user_fields_to_export,
        }
        result = self._make_api_call("POST", "users/export/ids", payload=payload)
        users = result.get("users", [])
        braze_users = [BrazeUser.model_validate(user) for user in users]
        return braze_users

    def get_users_by_external_ids(self, external_ids: list[str]) -> list[BrazeUser]:
        payload = {
            "external_ids": external_ids,
            "fields_to_export": self._user_fields_to_export,
        }
        result = self._make_api_call("POST", "users/export/ids", payload=payload)
        users = result.get("users", [])
        braze_users = [BrazeUser.model_validate(user) for user in users]
        return braze_users

    def merge_users_by_external_ids(self, merge_request: BrazeMergeUsersRequest) -> str:

        merge_status = self._make_api_call(
            "POST", "users/merge", payload=merge_request.model_dump()
        )
        return merge_status["message"]
