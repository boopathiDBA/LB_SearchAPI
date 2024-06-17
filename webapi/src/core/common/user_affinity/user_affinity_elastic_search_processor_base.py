from abc import abstractmethod, ABCMeta
from typing import TypeVar

from src.adapters.elastic_search.elastic_search_client import ElasticSearchResult
from src.adapters.elastic_search.elastic_search_processor import (
    ElasticSearchQuery,
    IElasticSearchProcessor,
    ElasticSearchProcessorBase,
)
from src.core.common.user_affinity.user_affinity_request import (
    UserAffinityRequest,
    GenderEnum,
)

TParsedResponse = TypeVar("TParsedResponse")

parse_response_return_type = list[dict]


class UserAffintiyElasticSearchProcessorBase(
    ElasticSearchProcessorBase[UserAffinityRequest, parse_response_return_type],
    IElasticSearchProcessor[UserAffinityRequest, parse_response_return_type],
    metaclass=ABCMeta,
):
    """This class holds common code that is reused by the UserAffinitySaleEventProcessor and UserAffinityVoucherProcessor."""

    @abstractmethod
    def _get_top_term(self) -> str:
        raise NotImplementedError()

    def generate_query(self, args: UserAffinityRequest) -> ElasticSearchQuery:
        query = {
            # The reason for returning 50 results is to allow for variation of the results to be applied to create
            # variety from the users perspective.
            "size": 50,
            "from": 0,
            "query": {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {self._get_top_term(): {"value": True}}},
                                {"range": {"score": {"gte": 0}}},
                                {"exists": {"field": "slug"}},
                            ],
                            "must_not": [],
                            "filter": [],
                        }
                    },
                    "script_score": {
                        "script": {
                            "id": "user-affinity-search",
                            "params": {
                                "items": self._get_affinity_items(args),
                                "gender": "",
                            },
                        }
                    },
                    "boost_mode": "replace",
                }
            },
        }
        self._maybe_apply_query_filter(args, query)
        self._maybe_apply_query_gender(args, query)

        return query

    def parse_response(
        self, response: ElasticSearchResult
    ) -> parse_response_return_type:
        try:
            sources = [hit["_source"] for hit in response["hits"]["hits"]]
            return self._filter_items(sources)
        except KeyError:
            return []

    def _filter_items(self, items: list[dict]) -> parse_response_return_type:
        """
        Filter the response to have no more than 1 one of the same retailer or category.
        If there are less than the desired minimum, repopulate the list with the duplicates.
        """
        final_list = self._remove_duplicates_by_attr(items, "store_id")
        final_list = self._remove_duplicates_by_attr(final_list, "category_id")

        DESIRED_MINIMUM = 3

        # Early break if we have enough items
        if len(final_list) >= DESIRED_MINIMUM:
            return final_list[:10]

        # minimum 3 items are required. Repopulate list until reaching minimum
        for item in items:
            if len(final_list) >= DESIRED_MINIMUM:
                break
            elif item not in final_list:
                final_list.append(item)

        return final_list

    def _remove_duplicates_by_attr(self, items: list, key: str) -> list:
        key_values_to_item_mapping = {}
        for item in items:
            if (key_value := item[key]) not in key_values_to_item_mapping:
                key_values_to_item_mapping[key_value] = item
        return list(key_values_to_item_mapping.values())

    def _maybe_apply_query_filter(
        self, args: UserAffinityRequest, query: ElasticSearchQuery
    ) -> None:
        query["query"]["function_score"]["query"]["bool"]["filter"] = [
            {
                # keyword has the suffix `s` removed. e.g. brand_names -> brand_name
                "terms": {f"{filter_key[:-1]}.keyword": filter_values}
            }
            for filter_key, filter_values in args
            if "names" in filter_key and len(filter_values) > 0
        ]

    def _maybe_apply_query_gender(
        self, args: UserAffinityRequest, query: ElasticSearchQuery
    ) -> None:
        if args.gender.lower() == GenderEnum.EMPTY:
            return

        gender_map = {GenderEnum.MALE: "M", GenderEnum.FEMALE: "F"}
        gender = gender_map[args.gender]

        query["query"]["function_score"]["query"]["bool"]["minimum_should_match"] = 1
        query["query"]["function_score"]["query"]["bool"]["should"] = [
            {"term": {"category_gender_affinity": {"value": gender}}},
            {
                "nested": {
                    "path": "object_properties",
                    "query": {
                        "term": {
                            "object_properties.category_gender_affinity": {
                                "value": gender
                            }
                        }
                    },
                }
            },
            {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "must_not": [
                                    {"exists": {"field": "category_gender_affinity"}}
                                ]
                            }
                        },
                        {
                            "bool": {
                                "must_not": [
                                    {
                                        "nested": {
                                            "path": "object_properties",
                                            "query": {
                                                "exists": {
                                                    "field": "object_properties.category_gender_affinity"
                                                }
                                            },
                                        }
                                    }
                                ]
                            }
                        },
                    ]
                }
            },
        ]

    def _plural_name_to_singular(self, name: str) -> str:
        """Given the name stores, brands, departments, categories, return the singular key. e.g store, category"""
        if name[-3:] == "ies":
            singular_key = name[:-3] + "y"
        elif name[-1] == "s":
            singular_key = name[:-1]
        else:
            raise ValueError(f"Unsupported plural to singular key: {name}")

        return singular_key

    def _get_affinity_items(self, args: UserAffinityRequest) -> list[dict]:
        if not args.affinity:
            return []
        else:
            return [
                {
                    "name": affinity.name,
                    "cscore": affinity.score,
                    "field": f"{self._plural_name_to_singular(affinity_name)}_name.keyword",
                }
                for affinity_name, affinities in args.affinity
                for affinity in affinities
            ]
