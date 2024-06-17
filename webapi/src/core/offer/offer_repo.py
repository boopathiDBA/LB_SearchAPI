from typing import Protocol
from src.adapters.elastic_search.elastic_search_client import (
    IElasticSearchClient,
    get_elastic_search_client,
)
from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.core.offer.offer_filter_options_elastic_search_processor import (
    OfferFilterOptionsElasticSearchProcessor,
)
from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    FilterOption,
)


class IOfferRepo(Protocol):  # pylint: disable=too-few-public-methods
    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        pass


class OfferRepo(IOfferRepo):  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        elastic_search_client: IElasticSearchClient = get_elastic_search_client(),
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ) -> None:
        self._elastic_search_client = elastic_search_client
        self._rds_client = rds_client

        self._offer_filter_options_elastic_search_processor = (
            OfferFilterOptionsElasticSearchProcessor()
        )

    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        filter_options = self._offer_filter_options_elastic_search_processor.execute(
            self._elastic_search_client, request
        )

        # sort descending by doc_count
        filter_options.sort(key=lambda x: x.doc_count, reverse=True)

        return filter_options
