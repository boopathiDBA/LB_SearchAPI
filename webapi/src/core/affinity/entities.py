from pydantic import Field

from src.common.base_model import BaseModel
from src.core.common.base_entity import BaseEntity


class AffinityDetails(BaseModel):
    name: str | None = Field(default=None, description="Name of the affinity object")
    score: float | None = Field(
        default=None, description="Score of the affinity object"
    )
    absolute: int | None = Field(
        default=None, description="Absolute value? of the affinity object"
    )


class Affinity(BaseModel):
    brands: list[AffinityDetails] | None = Field(
        default=[], description="Brand affinity details"
    )
    stores: list[AffinityDetails] | None = Field(
        default=[], description="Stores affinity details"
    )
    departments: list[AffinityDetails] | None = Field(
        default=[], description="Departments affinity details"
    )
    categories: list[AffinityDetails] | None = Field(
        default=[], description="Categories affinity details"
    )
    subcategories: list[AffinityDetails] | None = Field(
        default=[], description="Subcategories affinity details"
    )


class ElasticSearchUserAffinity(BaseEntity):
    """
    Structure of the Opensearch Doc
    """

    user_id: int | None = Field(description="User id of the affinity data")
    network_userids: list[str] | None = Field(
        default=[], description="Network user ids of the affinity data"
    )
    # Result from open search may be null
    gender: str | None = Field(default=None, description="Gender details of the user")
    affinity: Affinity | None = Field(
        default=None, description="Affinity details of the user"
    )
