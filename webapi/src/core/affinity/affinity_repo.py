"""
This repository is related to Affinity Elasticsearch and RDS Queries
"""

from typing import Protocol

from src.adapters.elastic_search.elastic_search_client import (
    IElasticSearchClient,
    get_elastic_search_client,
)
from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from .entities import ElasticSearchUserAffinity, AffinityDetails, Affinity
from ..common.context import Context
from ...adapters.elastic_search.queries.helper import ElasticSearchIndexEnum


class IAffinityRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Elastic search Affinity interface
    """

    def elastic_search_by_user_id_or_network_userid(
        self, user_id: str | None, network_userid: str | None, context: Context = None
    ) -> ElasticSearchUserAffinity | None:
        """
        Elastic search by user_id or network_userid for affinities.
        """


class AffinityRepo(IAffinityRepo):  # pylint: disable=too-few-public-methods
    """
    AffinityRepo class for Opensearch and related methods
    """

    def __init__(
        self,
        elastic_search_client: (
            IElasticSearchClient | None
        ) = get_elastic_search_client(),
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._elastic_search_client = elastic_search_client
        self._rds_client = rds_client

    def elastic_search_by_user_id_or_network_userid(
        self, user_id: str | None, network_userid: str | None, context: Context = None
    ) -> ElasticSearchUserAffinity | None:
        result = None

        # If only user_id is given and no network_userid
        if user_id and not network_userid:
            result = self._elastic_search_by_user_id(user_id)

        # If only network_userid is given and no user_id
        if result is None and network_userid and not user_id:
            result = self._elastic_search_by_network_userid(network_userid)

        # If both user_id and network_userid are given
        if result is None and user_id and network_userid:
            result = self._elastic_search_by_user_id(user_id)
            if result is None:
                result = self._elastic_search_by_network_userid(network_userid)

        # If no results from above, fetch affinity data from webdb
        if result is None and context and context.user_id:
            result = self._rds_search_by_user_id(context.user_id)

        return result

    def _elastic_search_by_user_id(
        self, user_id: str
    ) -> ElasticSearchUserAffinity | None:
        query = {
            "query": {
                "bool": {
                    "filter": [{"term": {"user_id": int(user_id) if user_id else None}}]
                }
            }
        }

        results = self._elastic_search_client.query_index(
            ElasticSearchIndexEnum.AFFINITY, query
        )

        return (
            ElasticSearchUserAffinity(**results["hits"]["hits"][0]["_source"])
            if len(results["hits"]["hits"]) > 0
            else None
        )

    def _elastic_search_by_network_userid(
        self, network_userid: str
    ) -> ElasticSearchUserAffinity:
        query = {
            "query": {
                "bool": {
                    "filter": [{"term": {"network_userids.keyword": network_userid}}]
                }
            }
        }

        results = self._elastic_search_client.query_index(
            ElasticSearchIndexEnum.AFFINITY, query
        )

        return (
            ElasticSearchUserAffinity(**results["hits"]["hits"][0]["_source"])
            if len(results["hits"]["hits"]) > 0
            else None
        )

    def _rds_search_by_user_id(self, user_id: str) -> ElasticSearchUserAffinity:
        user_query = f"""
                        SELECT gender
                        FROM users
                        where id=%s;
                    """
        user_query_values = [int(user_id)]
        user_results = self._rds_client.execute_fetch_all_query(
            user_query, user_query_values
        )

        result = ElasticSearchUserAffinity(
            user_id=int(user_id),
            gender=user_results[0][0] if len(user_results) > 0 else "",
        )

        followable_types = {
            "Brand": "brands",
            "Store": "stores",
            "Department": "departments",
            "Category": "categories",
            "Subcategory": "subcategories",
        }
        affinity = {}

        # TODO: Currently this does multiple calls to db. We should be able to reduce this to one?
        for followable_type, table in followable_types.items():
            sql_query = f"""
                SELECT x.name
                FROM follows as f
                left join {table} as x on f.followable_id=x.id
                where user_id=%s and followable_type=%s;
            """
            values = [int(user_id), followable_type]
            results = self._rds_client.execute_fetch_all_query(sql_query, values)

            affinity[table] = [
                AffinityDetails(name=result[0], score=1, absolute=0)
                for result in results
            ]

        result.affinity = Affinity(**affinity)
        return result
