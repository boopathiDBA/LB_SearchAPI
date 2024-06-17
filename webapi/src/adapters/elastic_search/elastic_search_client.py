import json
import os
from datetime import datetime
from typing import Protocol, TypeAlias

import requests

from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum


class ElasticSearchRequestException(Exception):
    pass


ElasticSearchResult: TypeAlias = dict[str, any]

QueryDsl: TypeAlias = dict | str


class ElasticSearchQueryDslEncoder(json.JSONEncoder):
    """Customer JSON encoder to handle types that are not serializable by default."""

    def default(self, obj: any) -> any:
        """Default is called by json.dumps() for objects that are not serializable"""

        # Opensearch expects datetime in isoformat
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class IElasticSearchClient(Protocol):
    def query_index(
        self, index: ElasticSearchIndexEnum, query_dsl: QueryDsl
    ) -> ElasticSearchResult:
        pass


class ElasticSearchClient(IElasticSearchClient):
    def __init__(self, elastic_search_host: str):
        self._elastic_search_host = elastic_search_host

    def query_index(
        self, index: ElasticSearchIndexEnum, query_dsl: QueryDsl
    ) -> ElasticSearchResult:
        """
        Parameters:
            index (ElasticSearchIndexEnum): Elastic search index to run query on.
            query_dsl (dict | str): Elastic search query. Depending on the incoming type,
                                    type casting will be handled appropriately
        Raises:
            ElasticSearchRequestException: If request to Elastic Search fails.
        """

        try:
            opensearch_url = f"{self._elastic_search_host}/{index}"
            headers = {"Content-Type": "application/json"}
            body_json = self._to_str(query_dsl)
            response = requests.get(
                url=opensearch_url, data=body_json, headers=headers, timeout=5
            )
        except Exception as e:
            raise ElasticSearchRequestException(str(e))

        if (status_code := response.status_code) != 200:
            raise ElasticSearchRequestException(
                f"Unexpected status code {status_code}. Request url: {opensearch_url}. Request body: {body_json}. "
                f"Response body: {response.text}."
            )

        return response.json()

    def _to_str(self, query_dsl: QueryDsl) -> str:
        if isinstance(query_dsl, dict):
            # Encode with custom encoder.
            # NOTE: avoid using the parameter `default` of `json.dumps()` here
            # instead, implement in ElasticSearchQueryDslEncoder
            return json.dumps(query_dsl, cls=ElasticSearchQueryDslEncoder)
        elif isinstance(query_dsl, str):
            return query_dsl
        else:
            raise ValueError(
                f"Unexpected type for query_dsl: {type(query_dsl)}. "
                f"Expected dict or str."
            )


def get_elastic_search_client() -> IElasticSearchClient:
    opensearch_host = os.getenv(
        "OPENSEARCH_HOST", "https://search.stream.littlebirdie.dev"
    )
    return ElasticSearchClient(opensearch_host)
