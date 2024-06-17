from src.adapters.elastic_search.elastic_search_processor import IElasticSearchProcessor
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.core.common.user_affinity.user_affinity_elastic_search_processor_base import (
    UserAffintiyElasticSearchProcessorBase,
)


class UserAffinitySaleEventsElasticSearchProcessor(
    UserAffintiyElasticSearchProcessorBase,
    IElasticSearchProcessor,
):
    """Elastic Search processor that generates a query to retrieve sales events based on user's affinity."""

    def get_index(self) -> ElasticSearchIndexEnum:
        return ElasticSearchIndexEnum.SALE_EVENT

    def _get_top_term(self) -> str:
        return "is_top_sale_event"
