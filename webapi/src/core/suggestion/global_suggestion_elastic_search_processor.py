import json

from src.adapters.elastic_search.elastic_search_client import (
    ElasticSearchResult,
)
from src.adapters.elastic_search.elastic_search_processor import (
    ElasticSearchProcessorBase,
    ElasticSearchQuery,
    IElasticSearchProcessor,
)
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.core.suggestion.entities import ElasticSearchSuggestion
from src.core.suggestion.suggestion_repo import GlobalSuggestionRequest


class GlobalSuggestionElasticSearchProcessor(
    ElasticSearchProcessorBase[GlobalSuggestionRequest, ElasticSearchSuggestion],
    IElasticSearchProcessor[GlobalSuggestionRequest, ElasticSearchSuggestion],
):
    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.MUTLI_SEARCH

    def generate_query(self, args: GlobalSuggestionRequest) -> ElasticSearchQuery:
        """Generate query for global suggestions.

        This query uses a company custom muti search index. One major
        difference with it its implementation is that the payload isn't the usual JSON format. Instead it's a string with newline characters separating the different queries.

        docs: https://opensearch.org/docs/latest/api-reference/multi-search/
        """
        template = []

        self._append_deals_autocomplete_template(
            template,
            {"id": "preemptive_autocomplete_template", "params": {"query": args.query}},
        )
        self._append_deals_autocomplete_template(
            template,
            {"id": "brand_autocomplete_template", "params": {"query": args.query}},
        )
        self._append_deals_autocomplete_template(
            template,
            {"id": "department_autocomplete_template", "params": {"query": args.query}},
        )
        self._append_deals_autocomplete_template(
            template,
            {"id": "product_autocomplete_template", "params": {"query": args.query}},
        )

        # Query production suggestions when pagecontext_key and pagecontext_value are provided
        if args.pagecontext_key and args.pagecontext_value:
            template.append({"index": "a_deals_autocomplete"})
            template.append(
                {
                    "id": "pagecontext_autocomplete_template",
                    "params": {
                        "query": args.query,
                        "pagecontext_key": f"{args.pagecontext_key}.keyword",
                        "pagecontext_value": args.pagecontext_value,
                    },
                }
            )

        template_str = ""
        for each in template:
            # Each line needs a newline character to be able to be parsed correctly with multi search
            template_str += "%s \r\n" % json.dumps(each)

        return template_str

    def _append_deals_autocomplete_template(
        self, template: list[dict], query: dict
    ) -> None:
        template.append({"index": "a_deals_autocomplete"})
        template.append(query)

    def parse_response(self, response: ElasticSearchResult) -> ElasticSearchSuggestion:
        aggregations_data_flattened = self._get_flatterned_aggregations_data(response)

        return ElasticSearchSuggestion.model_validate(
            {
                "preemptive_category_suggestion": {
                    "data": (
                        self._get_suggestion_key_count_from_results(
                            name="preemptive_category_suggestion",
                            aggregation_data=aggregations_data_flattened,
                        )
                    )
                },
                "preemptive_subcategory_suggestion": {
                    "data": (
                        self._get_suggestion_key_count_from_results(
                            name="preemptive_subcategory_suggestion",
                            aggregation_data=aggregations_data_flattened,
                        )
                    )
                },
                "store_main": {
                    "data": self._get_suggestion_main_data_from_results(
                        name="store", aggregations_data=aggregations_data_flattened
                    )
                },
                "brand_main": {
                    "data": self._get_suggestion_main_data_from_results(
                        name="brand", aggregations_data=aggregations_data_flattened
                    )
                },
                "category_main": {
                    "data": self._get_suggestion_main_data_from_results(
                        name="category", aggregations_data=aggregations_data_flattened
                    )
                },
                "department_main": {
                    "data": self._get_suggestion_main_data_from_results(
                        name="department", aggregations_data=aggregations_data_flattened
                    )
                },
                "subcategory_main": {
                    "data": self._get_suggestion_main_data_from_results(
                        name="subcategory",
                        aggregations_data=aggregations_data_flattened,
                    )
                },
                "pagecontext_suggest": {
                    "data": self._get_suggestion_key_count_from_results(
                        name="pagecontext_suggest",
                        aggregation_data=aggregations_data_flattened,
                    )
                },
                "product_suggestion": {
                    "data": self._get_suggestion_key_count_from_results(
                        name="product_suggestion",
                        aggregation_data=aggregations_data_flattened,
                    )
                },
            }
        )

    def _get_flatterned_aggregations_data(
        self,
        results: ElasticSearchResult,
    ) -> dict[str, any]:
        flattened_aggregations_data = {}

        for response in results["responses"]:
            try:
                aggregations = response["aggregations"]
            except KeyError:
                # Reaches here if there is an error response from opensearch since
                # TODO: log error
                continue

            for key, value in response["aggregations"].items():
                flattened_aggregations_data[key] = value

        return flattened_aggregations_data

    def _get_suggestion_main_data_from_results(
        self, *, name: str, aggregations_data: dict[str, any]
    ) -> list[dict]:
        try:
            return [
                bucket[f"{name}_details"]["hits"]["hits"][0]
                for bucket in aggregations_data[f"{name}_main"][f"{name}_suggestion"][
                    "buckets"
                ]
            ]
        # If opensearch returns an error response we should reach here
        except KeyError:
            # TODO log error
            return []

    def _get_suggestion_key_count_from_results(
        self, *, name: str, aggregation_data: dict[str, any]
    ) -> list[dict[str, any]]:
        try:
            return aggregation_data[name]["buckets"]
        # If opensearch returns an error response we should reach here
        except KeyError:
            # TODO log error
            return []
