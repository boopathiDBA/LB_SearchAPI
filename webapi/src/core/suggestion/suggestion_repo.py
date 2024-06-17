from typing import Protocol

from pydantic import Field, model_validator

from src.adapters.elastic_search.elastic_search_client import (
    get_elastic_search_client,
    IElasticSearchClient,
)
from src.common.base_model import BaseModel
from src.core.suggestion.entities import ElasticSearchSuggestion


class GlobalSuggestionRequest(BaseModel):
    query: str = Field(description="Query to search by", examples=["nike"])
    pagecontext_key: str | None = Field(
        default=None,
        description="Key to use for page context",
        examples=["department_name"],
    )
    pagecontext_value: str | None = Field(
        default=None,
        description="Value to use for page context",
        examples=["Electronics"],
    )

    @model_validator(mode="after")
    def _validate_pagecontext_key_and_value(self) -> "GlobalSuggestionRequest":
        """Validate when either pagecontext_key or pagecontext_value is provided
        that both must be provided"""
        if self.pagecontext_key or self.pagecontext_value:
            if self.pagecontext_key is None or self.pagecontext_value is None:
                raise ValueError(
                    "Both pagecontext_key and pagecontext_value must be provided"
                )
        return self


class ISuggestionRepo(Protocol):  # pylint: disable=too-few-public-methods
    def get_global_suggestions(
        self, request: GlobalSuggestionRequest
    ) -> ElasticSearchSuggestion:
        pass


class SuggestionRepo(ISuggestionRepo):
    def __init__(
        self, elastic_search_client: IElasticSearchClient = get_elastic_search_client()
    ):
        self._elastic_search_client = elastic_search_client

        # Import here to avoid circular import
        from src.core.suggestion.global_suggestion_elastic_search_processor import (
            GlobalSuggestionElasticSearchProcessor,
        )

        self._global_suggestion_elastic_search_processor = (
            GlobalSuggestionElasticSearchProcessor()
        )
        pass

    def get_global_suggestions(
        self, request: GlobalSuggestionRequest
    ) -> ElasticSearchSuggestion:
        return self._global_suggestion_elastic_search_processor.execute(
            self._elastic_search_client, request
        )
