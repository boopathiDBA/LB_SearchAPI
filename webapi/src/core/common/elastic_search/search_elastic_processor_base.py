from abc import ABCMeta, abstractmethod

from pydantic import Field

from src.adapters.elastic_search.elastic_search_client import ElasticSearchResult
from src.adapters.elastic_search.elastic_search_processor import (
    ElasticSearchProcessorBase,
    ElasticSearchQuery,
    IElasticSearchProcessor,
)
from src.common.base_model import BaseModel

parse_response_return_type = list[dict]


class ElasticSearchRequest(BaseModel):
    query: str
    per_page: int
    # TODO: Handle from
    from_field: int = Field(..., alias="from")
    order: str | None
    value: str | None
    store_names: list[str] = []
    brand_names: list[str] = []
    department_names: list[str] = []
    category_names: list[str] = []
    subcategory_names: list[str] = []


class SearchElasticProcessorBase(
    ElasticSearchProcessorBase[ElasticSearchRequest, parse_response_return_type],
    IElasticSearchProcessor[ElasticSearchRequest, parse_response_return_type],
    metaclass=ABCMeta,
):
    """Base class for Elastic searching for vouchers and sale events."""

    @abstractmethod
    def _get_query_id(self) -> str:
        raise NotImplementedError()

    def generate_query(self, args: ElasticSearchRequest) -> ElasticSearchQuery:
        query = {
            "id": self._get_query_id(),
            "params": {
                "query": args.query,
                "size": args.per_page,
                "from": args.from_field,
                "sort": [],
                "filter": {"filter": []},
            },
        }

        self._apply_filter(query, args)

        return query

    def _apply_filter(self, query: dict, args: ElasticSearchRequest) -> dict:
        if args.brand_names:
            query["params"]["filter"]["filter"].append(
                {
                    "nested": {
                        "path": "brands",
                        "query": {
                            "terms": {"brands.brand_name.keyword": args.brand_names}
                        },
                    }
                }
            )
        elif args.department_names:
            query["params"]["filter"]["filter"].append(
                {
                    "nested": {
                        "path": "object_properties",
                        "query": {
                            "terms": {
                                "object_properties.department_name.keyword": args.department_names
                            }
                        },
                    }
                }
            )
        elif args.category_names:
            query["params"]["filter"]["filter"].append(
                {
                    "nested": {
                        "path": "object_properties",
                        "query": {
                            "terms": {
                                "object_properties.category_name.keyword": args.category_names
                            }
                        },
                    }
                }
            )
        elif args.store_names:
            query["params"]["filter"]["filter"].append(
                {"terms": {"store_name.keyword": args.store_names}}
            )

        return query

    def parse_response(
        self, response: ElasticSearchResult
    ) -> parse_response_return_type:
        return [hit["_source"] for hit in response["hits"]["hits"]]
