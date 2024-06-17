from datetime import datetime
from enum import StrEnum

from pydantic import Field

from src.adapters.elastic_search.elastic_search_client import (
    ElasticSearchResult,
    get_elastic_search_client,
)
from src.adapters.elastic_search.elastic_search_template import ElasticSearchTemplate
from src.adapters.elastic_search.queries.helper import (
    apply_filter,
    ElasticSearchFilterOptions,
    ElasticSearchIndexEnum,
)
from src.common.base_model import BaseModel


class FieldEnum(StrEnum):
    STORE_NAME = "store_name"
    BRAND_NAME = "brand_name"
    CATEGORY_NAME = "category_name"
    DEPARTMENT_NAME = "department_name"
    SUBCATEGORY_NAME = "subcategory_name"


class FilterOptionsIdEnum(StrEnum):
    VOUCHER_SEARCH = "voucher_search"
    SALE_EVENT_SEARCH = "sale_event_search"
    OFFER_SEARCH_V2 = "deal_search_v2"

    def get_elastic_search_index(self) -> ElasticSearchIndexEnum:
        """Return the index name for the given filter options id."""
        if self == FilterOptionsIdEnum.VOUCHER_SEARCH:
            return ElasticSearchIndexEnum.VOUCHER_TEMPLATE
        elif self == FilterOptionsIdEnum.SALE_EVENT_SEARCH:
            return ElasticSearchIndexEnum.SALE_EVENT_TEMPLATE
        elif self == FilterOptionsIdEnum.OFFER_SEARCH_V2:
            return ElasticSearchIndexEnum.OFFER_TEMPLATE
        else:
            raise ValueError(f"FilterOptionsIdEnum {self} not supported")


class ElasticSearchFilterOptionsRequest(BaseModel):
    # This currently is mapped to our implementation of Elastic search query that requires an id field. eg. `voucher_search`
    id: FilterOptionsIdEnum
    store_name: list[str] = Field(
        default=[], description="Filter by store names", examples=["Catch"]
    )
    brand_name: list[str] = Field(
        default=[], description="Filter by brand names", examples=["Adidas"]
    )
    category_name: list[str] = Field(
        default=[], description="Filter by category names", examples=["Backpacks"]
    )
    department_name: list[str] = Field(
        default=[], description="Filter by department names", examples=["Fashion"]
    )
    subcategory_name: list[str] = Field(
        default=[], description="Filter by subcategory names"
    )
    query: str = Field(description="Query to search by", examples=["20% off"])
    field: FieldEnum = Field(description="Field to search by")
    is_top_deal: bool = Field(default=True, description="Search top deals")
    per_page: int = Field(default=50, description="Number of items per page")
    last_price_date: list[datetime] = Field(
        default=[],
        description="Array of last price update range [maxAge, minAge]",
    )
    price: list[int] = Field(
        default=[],
        description="Array of price range [minPrice, maxPrice]",
    )
    price_shift: list[float] = Field(
        default=[],
        description="Array of discount range [maxDiscount, minDiscount]",
    )
    fuzzy_search: bool = Field(
        default=False, description="Determines whether to fuzzy search"
    )

    def to_elastic_search_filter_options(self) -> ElasticSearchFilterOptions:
        """Factory method that return instance from ElasticSearchFilterOptions.
        Currently, the keys from ElasticSearchFilterOptions only differ by a missing `s`.
        """
        return ElasticSearchFilterOptions(
            **{f"{key}s": value for key, value in dict(self).items()}
        )


class FilterOption(BaseModel):
    key: str
    doc_count: int


def query_filter_options(
    request: ElasticSearchFilterOptionsRequest,
) -> list[FilterOption]:
    template = ElasticSearchTemplate(template_file_name="filter_options_template.json")
    template_query = template.apply_data(request)

    template_query = _update_aggregation(template_query, request)

    template_query = apply_filter(
        template_query, request.to_elastic_search_filter_options()
    )

    results = get_elastic_search_client().query_index(
        request.id.get_elastic_search_index(), template_query
    )

    filter_options = _get_nested_aggregates(request.field, results)

    filter_options = [
        {
            "key": option["key"],
            "doc_count": (
                option["unique_count"]["value"]
                # NOTE: uncomment below when implementing offer search
                # if request.id is FilterOptionsIdEnum.OFFER_SEARCH_V2
                if "unique_count" in option and "value" in option["unique_count"]
                else option["doc_count"]
            ),
        }
        for option in filter_options
    ]

    # sort descending by doc_count
    filter_options.sort(key=lambda x: int(x["doc_count"]), reverse=True)

    return [FilterOption(**kwargs) for kwargs in filter_options]


def _update_aggregation(
    template_query: dict, request: ElasticSearchFilterOptionsRequest
) -> dict:
    """Given the request field, add an aggregation.

    Currently, all Fields yield the same aggregation except for `department_name`
    where reversed is applied.
    """
    # Defaulting to 500 for brand_name and store_name since pagination breaks in the front end,
    # so we return 500 and let the front end handle pagination.
    size = 500 if request.field in ("brand_name", "store_name") else request.per_page

    # Add a aggregation for the field
    template_query["params"]["aggs"][request.field.value] = {
        "terms": {"field": f"{request.field.value}.keyword", "size": size},
        "aggs": {"unique_count": {"cardinality": {"field": "id"}}},
    }

    return template_query


def _get_nested_aggregates(
    field: FieldEnum, results: ElasticSearchResult
) -> list[dict[str, any]]:
    """Return buckets response for a given field from results.

    This currently checks if there is a nested configured and finds the buckets appropriately.
    """
    if field is FieldEnum.BRAND_NAME:
        return results["aggregations"]["brands"]["nested_brand"]["buckets"]
    elif field is FieldEnum.STORE_NAME:
        return results["aggregations"]["stores"]["buckets"]
    elif field is FieldEnum.CATEGORY_NAME:
        return results["aggregations"]["categories"]["nested_categories"]["buckets"]
    elif field is FieldEnum.DEPARTMENT_NAME:
        return results["aggregations"]["departments"]["nested_dept"]["buckets"]
    elif field is FieldEnum.SUBCATEGORY_NAME:
        return results["aggregations"]["subcategory_name"]["buckets"]
    else:
        raise Exception(f"Unsupported field: {str(field)}")

    # field_aggregation_result = results["aggregations"][field.value]
    # if "nested" in field_aggregation_result.keys():
    #     return field_aggregation_result["nested"]["buckets"]
    # else:
    #     return field_aggregation_result["buckets"]
