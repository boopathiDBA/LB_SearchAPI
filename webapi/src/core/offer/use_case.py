from src.core.offer.offer_repo import IOfferRepo, OfferRepo
from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    FilterOption,
)


def get_offer_filter_options(
    request: ElasticSearchFilterOptionsRequest,
    offer_repo: IOfferRepo = OfferRepo(),
) -> list[FilterOption]:
    if filter_options := offer_repo.get_filter_options(request):
        return filter_options
    else:
        # If no filter options are found with strict query search then perform a fuzzy search
        request.fuzzy_search = True
        return offer_repo.get_filter_options(request)
