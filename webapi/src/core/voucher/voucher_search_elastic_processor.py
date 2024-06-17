from src.adapters.elastic_search.elastic_search_processor import IElasticSearchProcessor
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.core.common.elastic_search.search_elastic_processor_base import (
    SearchElasticProcessorBase,
)


class VoucherSearchElasticProcessor(
    SearchElasticProcessorBase,
    IElasticSearchProcessor,
):
    """Elastic Search processor that generates a query to retrieve vouchers."""

    def _get_query_id(self) -> str:
        return "voucher_search"

    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.VOUCHER_TEMPLATE
