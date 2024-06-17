from src.adapters.elastic_search.elastic_search_processor import IElasticSearchProcessor
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.core.common.user_affinity.user_affinity_elastic_search_processor_base import (
    UserAffintiyElasticSearchProcessorBase,
)


class UserAffinityVouchersSearchElasticProcessor(
    UserAffintiyElasticSearchProcessorBase,
    IElasticSearchProcessor,
):
    """Elastic Search processor that generates a query to retrieve vouchers based on user's affinity."""

    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.VOUCHER

    def _get_top_term(self) -> str:
        return "is_top_voucher"
