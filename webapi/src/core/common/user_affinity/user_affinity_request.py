from enum import StrEnum

from pydantic import Field, field_validator

from src.common.base_model import BaseModel


class GenderEnum(StrEnum):
    MALE = "male"
    FEMALE = "female"
    EMPTY = ""  # Allow for empty string


class AffinityConfigurationRequest(BaseModel):
    name: str
    score: float
    absolute: int


class AffinityRequest(BaseModel):
    brands: list[AffinityConfigurationRequest] = Field(default=[])
    stores: list[AffinityConfigurationRequest] = Field(default=[])
    departments: list[AffinityConfigurationRequest] = Field(default=[])
    categories: list[AffinityConfigurationRequest] = Field(default=[])
    subcategories: list[AffinityConfigurationRequest] = Field(default=[])


class UserAffinityRequest(BaseModel):
    gender: GenderEnum | None = Field(
        default=GenderEnum.EMPTY, description="Gender to filter for"
    )
    affinity: AffinityRequest | None = Field(
        default=None, description="Affinity details to search for"
    )
    store_names: list[str] = Field(default=[], description="Store names to filter by")
    brand_names: list[str] = Field(default=[], description="Brand names to filter by")
    department_names: list[str] = Field(
        default=[], description="Department names to filter by"
    )
    category_names: list[str] = Field(
        default=[], description="Category names to filter by"
    )
    subcategory_names: list[str] = Field(
        default=[], description="Subcategory names to filter by"
    )

    @field_validator("gender", mode="before")
    @classmethod
    def _maybe_set_gender(cls, gender: any) -> str | None:
        """If gender is a string and is not empty,
        convert to lower case"""
        if isinstance(gender, str):
            return gender.lower()
        else:
            return gender

    @field_validator("affinity", mode="before")
    @classmethod
    def _maybe_set_affinity(cls, affinity: any) -> dict | None:
        """If the affinity is an empty dict, convert it to None."""
        if isinstance(affinity, dict) and len(affinity) == 0:
            return None
        else:
            return affinity
