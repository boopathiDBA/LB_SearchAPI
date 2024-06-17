from pydantic import Field, model_validator

from src.core.common.context import Context
from .affinity_repo import IAffinityRepo, AffinityRepo
from .entities import ElasticSearchUserAffinity
from ...common.base_model import BaseModel


class SearchElasticAffinityRequest(BaseModel):
    user_id: str | None = Field(
        default=None, description="user id to fetch the affinity details"
    )
    network_userid: str | None = Field(
        default=None, description="network userid to fetch the affinity details"
    )

    @model_validator(mode="after")
    def check_user_or_network_userid(self):
        if not self.user_id and not self.network_userid:
            raise ValueError("Either user_id or network_userid is required")
        return self


def elastic_search_affinity(
    request: SearchElasticAffinityRequest,
    context: Context,
    affinity_repo: IAffinityRepo = AffinityRepo(),
) -> ElasticSearchUserAffinity | None:
    return affinity_repo.elastic_search_by_user_id_or_network_userid(
        request.user_id, request.network_userid, context
    )
