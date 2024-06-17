from typing import TypeAlias
from src.adapters.elastic_search.elastic_search_client import ElasticSearchResult
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    FilterOption,
)
from src.adapters.elastic_search.elastic_search_processor import (
    ElasticSearchProcessorBase,
    ElasticSearchQuery,
    IElasticSearchProcessor,
)


ResponseType: TypeAlias = list[FilterOption]


class OfferFilterOptionsElasticSearchProcessor(
    ElasticSearchProcessorBase[ElasticSearchFilterOptionsRequest, ResponseType],
    IElasticSearchProcessor[ElasticSearchFilterOptionsRequest, ResponseType],
):

    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.OFFER_TEMPLATE

    def generate_query(
        self, args: ElasticSearchFilterOptionsRequest
    ) -> ElasticSearchQuery:
        query = {
            "id": args.id,
            "params": {
                "query": args.query,
                "size": 0,
                "filter": {"bool": {"must": [{"term": {"hide": False}}]}},
                "aggs": {},
            },
        }

        size = 500 if args.field in ("brand_name", "store_name") else args.per_page

        query["params"]["aggs"][args.field.value] = {
            "terms": {"field": f"{args.field}.keyword", "size": size},
            "aggs": {"unique_count": {"cardinality": {"field": "product_id"}}},
        }

        query = self._maybe_apply_ranges(args, query)
        query = self._maybe_apply_filters(args, query)

        # If fuzzy search is enabled, disregard the query and use fuzzyquery
        # NOTE: This generally happens when no results are found with the strict query search
        # and this Proccessor is called again but with fuzzy_search enabled
        if args.fuzzy_search:
            query["params"]["fuzzyquery"] = args.query
            del query["params"]["query"]

        return query

    def _maybe_apply_ranges(
        self, args: ElasticSearchFilterOptionsRequest, query: ElasticSearchQuery
    ) -> ElasticSearchQuery:
        for key in ("price", "last_price_date", "price_shift"):
            if range_value := getattr(args, key):
                first_range_elements, second_range_elements = range_value
                query["params"]["filter"]["bool"]["must"].append(
                    {
                        "range": {
                            key: {
                                "gte": first_range_elements,
                                "lte": second_range_elements,
                            }
                        }
                    }
                )

        return query

    def _maybe_apply_filters(
        self, args: ElasticSearchFilterOptionsRequest, query: ElasticSearchQuery
    ) -> ElasticSearchQuery:
        for key in (
            "store_name",
            "brand_name",
            "department_name",
            "category_name",
            "subcategory_name",
        ):
            if value := getattr(args, key):
                query["params"]["filter"]["bool"]["must"].append(
                    {"terms": {f"{key}.keyword": value}}
                )

        return query

    def parse_response(self, response: ElasticSearchResult) -> ResponseType:
        field_with_results = tuple(response["aggregations"].keys())
        assert len(field_with_results) <= 1, "Results should have zero or one result"

        # Return empty list if no results are found
        if not field_with_results:
            return []
        else:
            return [
                FilterOption.model_validate(
                    {"key": result["key"], "doc_count": result["unique_count"]["value"]}
                )
                for result in response["aggregations"][field_with_results[0]]["buckets"]
            ]
