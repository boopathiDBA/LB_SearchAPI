from enum import StrEnum

from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    FilterOption,
)
from src.core.brand.brand_repo import IBrandRepo, BrandRepo
from src.core.category.category_repo import ICategoryRepo, CategoryRepo
from src.core.common.context import Context
from src.core.common.elastic_search.search_elastic_processor_base import (
    ElasticSearchRequest,
)
from src.core.common.repository import Page, Order, OrderDirectionEnum, FriendlyId
from src.core.common.use_case import get_combined_entity_ids
from src.core.common.user_affinity.user_affinity_request import UserAffinityRequest
from src.core.department.department_repo import IDepartmentRepo, DepartmentRepo
from src.core.sale_event.entities import (
    ElasticSearchSaleEvent,
    ElasticSearchUserAffinitySaleEvent,
    SaleEvent,
)
from src.core.sale_event.sale_event_repo import ISaleEventRepo, SaleEventRepo
from src.core.store.store_repo import IStoreRepo, StoreRepo
from src.core.user.user_repo import IUserRepo, UserRepo
from src.core.vote.vote_repo import VotesRepo, IVotesRepo, VotableTypeEnum


class TopSaleEventsOrderColumnEnum(StrEnum):
    RANK = "rank"
    FIXED_GLOBAL_SCORE = "fixed_global_score"
    NAME = "name"
    PUBLISHED_AT = "published_at"


TOP_SALE_EVENTS_DEFAULT_PAGE = Page(page_number=1, per_page=50)
TOP_SALE_EVENTS_DEFAULT_ORDER = Order(
    column=TopSaleEventsOrderColumnEnum.RANK, direction=OrderDirectionEnum.ASC
)


def _maybe_update_sale_event_upvoted(
    sale_events: list[ElasticSearchSaleEvent], vote_ids: list[str]
) -> list[ElasticSearchSaleEvent]:
    if not vote_ids:
        return sale_events

    for sale_event in sale_events:
        if sale_event.id in vote_ids:
            sale_event.upvoted = True
    return sale_events


def elastic_search_sale_events(
    request: ElasticSearchRequest,
    context: Context,
    sale_event_repo: ISaleEventRepo = SaleEventRepo(),
    votes_repo: IVotesRepo = VotesRepo(),
) -> list[ElasticSearchSaleEvent]:
    sale_events = sale_event_repo.elastic_search(request)
    if context.user_id:
        vote_ids = votes_repo.get_votable_ids_for_user(
            context.user_id, VotableTypeEnum.SALE_EVENT
        )
        _maybe_update_sale_event_upvoted(sale_events, vote_ids)
    return sale_events


def get_sale_event_filter_options(
    request: ElasticSearchFilterOptionsRequest,
    sale_event_repo: ISaleEventRepo = SaleEventRepo(),
) -> list[FilterOption]:
    return sale_event_repo.get_filter_options(request)


def get_user_affinity_sale_events(
    request: UserAffinityRequest, sale_event_repo: ISaleEventRepo = SaleEventRepo()
) -> list[ElasticSearchUserAffinitySaleEvent]:
    return sale_event_repo.get_user_affinity_sale_events(request)


def get_unexpired_published_cba_sale_event(
    sale_event_repo: ISaleEventRepo = SaleEventRepo(),
) -> list[SaleEvent]:
    return sale_event_repo.get_unexpired_published_cba_sale_event()


def get_top_sale_events(
    *,
    page: Page = TOP_SALE_EVENTS_DEFAULT_PAGE,
    order: Order = TOP_SALE_EVENTS_DEFAULT_ORDER,
    by_department: FriendlyId | None = None,
    by_departments: set[str] | None = None,
    by_category: FriendlyId | None = None,
    by_categories: set[str] | None = None,
    by_store: FriendlyId | None = None,
    by_stores: set[str] | None = None,
    by_brand: FriendlyId | None = None,
    by_brands: set[str] | None = None,
    current: bool | None = None,
    upcoming: bool | None = None,
    by_followed_user: str | None = None,
    department_repo: IDepartmentRepo = DepartmentRepo(),
    category_repo: ICategoryRepo = CategoryRepo(),
    store_repo: IStoreRepo = StoreRepo(),
    brand_repo: IBrandRepo = BrandRepo(),
    sale_event_repo: ISaleEventRepo = SaleEventRepo(),
    user_repo: IUserRepo = UserRepo(),
) -> list[SaleEvent]:
    department_id = department_ids = None
    if by_department:
        department_id = department_repo.get_id_by_friendly_id(by_department)
    elif by_departments:
        department_ids = by_departments.copy()

    category = category_ids = None
    if by_category:
        category = category_repo.get_by_friendly_id(by_category)
    elif by_categories:
        category_ids = by_categories.copy()

    """
    Either single by_store is present,
        then fetch id by friendly_id and use as filter,
    Or multiple store ids are present,
        then use those ids as filter
    Same logic is applied to brands    
    """
    store_ids = get_combined_entity_ids(by_store, by_stores, store_repo)
    brand_ids = get_combined_entity_ids(by_brand, by_brands, brand_repo)

    if by_followed_user:
        # Filter by all store ids followed by this user
        if user_id := user_repo.get_id_by_friendly_id(by_followed_user):
            if followed_store_ids := store_repo.get_ids_followed_by_user_id(user_id):
                # Add followed store ids to the set if it already exists, else create new
                if store_ids:
                    store_ids.update(followed_store_ids)
                else:
                    store_ids = set(followed_store_ids)

    return sale_event_repo.get_top_sale_events(
        page=page,
        order=order,
        department_id=department_id,
        department_ids=department_ids,
        category=category,
        category_ids=category_ids,
        store_ids=store_ids,
        brand_ids=brand_ids,
        current=current,
        upcoming=upcoming,
    )


def get_sale_events_by_ids(
    sale_event_ids: list[str], sale_event_repo: ISaleEventRepo = SaleEventRepo()
) -> list[SaleEvent]:
    return sale_event_repo.get_by_ids(sale_event_ids)
