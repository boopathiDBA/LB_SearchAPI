from enum import StrEnum

from src.common.base_model import BaseModel


class ElasticSearchIndexEnum(StrEnum):
    VOUCHER_TEMPLATE = "a_vouchers/_search/template"
    SALE_EVENT_TEMPLATE = "a_sale_events/_search/template"
    OFFER_TEMPLATE = "a_deals/_search/template"
    VOUCHER = "a_vouchers/_search"
    SALE_EVENT = "a_sale_events/_search"
    MUTLI_SEARCH = "_msearch/template"
    AFFINITY = "a_affinity/_search"


class ElasticSearchFilterOptions(BaseModel):
    store_names: list[str] = []
    brand_names: list[str] = []
    department_names: list[str] = []
    category_names: list[str] = []
    subcategory_names: list[str] = []


def apply_filter(
    template_query: dict, filter_options: ElasticSearchFilterOptions
) -> dict:
    if filter_options.brand_names:
        template_query["params"]["filter"]["filter"] = {
            "nested": {
                "path": "brands",
                "query": {
                    "terms": {"brands.brand_name.keyword": filter_options.brand_names}
                },
            }
        }
    elif filter_options.department_names:
        template_query["params"]["filter"]["filter"] = {
            "nested": {
                "path": "object_properties",
                "query": {
                    "terms": {
                        "object_properties.department_name.keyword": filter_options.department_names
                    }
                },
            }
        }
    elif filter_options.category_names:
        template_query["params"]["filter"]["filter"] = {
            "nested": {
                "path": "object_properties",
                "query": {
                    "terms": {
                        "object_properties.category_name.keyword": filter_options.category_names
                    }
                },
            }
        }
    elif filter_options.store_names:
        template_query["params"]["filter"]["filter"] = {
            "terms": {"store_name.keyword": filter_options.store_names}
        }
    return template_query
