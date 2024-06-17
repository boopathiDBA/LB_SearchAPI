from typing import Any
from pydantic import Field
from datetime import datetime
from src.core.common.base_entity import BaseEntity


class BrazeUserAlias(BaseEntity):
    alias_name: str
    alias_label: str


class BrazeUser(BaseEntity):
    """
    The braze fields mentioned below are sourced from the braze get user API documentation available at under
    "Fields to export" section in the following link.

    https://documenter.getpostman.com/view/4689407/SVYrsdsG?version=latest#b9750447-9d94-4263-967f-f816f0c76577.
    """

    external_id: str = Field(description="Braze user id")
    braze_id: str
    first_name: str | None = Field(default=None)
    custom_attributes: dict[str, Any] | None = Field(
        default=None,
        description="""Braze custom attributes have the flexibility
                                                      to encompass a wide range of attributes, making it challenging
                                                      to define a specific model. Therefore, we've chosen to maintain
                                                      these custom_attributes in a generic format to facilitate the
                                                      addition of new custom attributes seamlessly""",
    )
    total_revenue: float
    user_aliases: list[BrazeUserAlias]
    created_at: datetime
