from src.adapters.elastic_search.elastic_search_processor import IElasticSearchProcessor
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.core.common.elastic_search.search_elastic_processor_base import (
    SearchElasticProcessorBase,
)


class SaleEventSearchElasticProcessor(
    SearchElasticProcessorBase,
    IElasticSearchProcessor,
):
    """Elastic Search processor that generates a query to retrieve sale events."""

    def _get_query_id(self) -> str:
        return "sale_events_search"

    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.SALE_EVENT_TEMPLATE
