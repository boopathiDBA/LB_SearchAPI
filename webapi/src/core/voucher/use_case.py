from enum import StrEnum

from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
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
from src.core.store.store_repo import IStoreRepo, StoreRepo
from src.core.user.user_repo import IUserRepo, UserRepo
from src.core.vote.vote_repo import IVotesRepo, VotesRepo, VotableTypeEnum
from src.core.voucher.entities import (
    ElasticSearchVoucher,
    Voucher,
    ElasticSearchUserAffinityVoucher,
    TopVoucherDBEntity,
)
from src.core.voucher.voucher_repo import (
    IVoucherRepo,
    VoucherRepo,
    FilterOption,
)
from src.delivery.http.router_helper import Request

"""
All fields of TopVoucherDBEntity are valid values for order_by[column] query param of top_lists/coupons api
This enum adds that validation
"""
TopVouchersOrderColumnEnum = StrEnum(
    "TopVouchersOrderColumnEnum", [*TopVoucherDBEntity.model_fields]
)

TOP_VOUCHERS_DEFAULT_PAGE = Page(page_number=1, per_page=50)
TOP_VOUCHERS_DEFAULT_ORDER = Order(column="rank", direction=OrderDirectionEnum.ASC)


def _maybe_update_voucher_upvoted(
    vouchers: list[ElasticSearchVoucher], vote_ids: list[str]
) -> list[ElasticSearchVoucher]:
    if not vote_ids:
        return vouchers

    for voucher in vouchers:
        if voucher.id in vote_ids:
            voucher.upvoted = True
    return vouchers


def elastic_search_vouchers(
    request: ElasticSearchRequest,
    context: Context,
    voucher_repo: IVoucherRepo = VoucherRepo(),
    votes_repo: IVotesRepo = VotesRepo(),
) -> list[ElasticSearchVoucher]:
    vouchers = voucher_repo.elastic_search(request)
    if context.user_id:
        vote_ids = votes_repo.get_votable_ids_for_user(
            context.user_id, VotableTypeEnum.VOUCHER
        )
        _maybe_update_voucher_upvoted(vouchers, vote_ids)
    return vouchers


def get_voucher_filter_options(
    request: ElasticSearchFilterOptionsRequest,
    voucher_repo: IVoucherRepo = VoucherRepo(),
) -> list[FilterOption]:
    return voucher_repo.get_filter_options(request)


def get_user_affinity_vouchers(
    request: UserAffinityRequest, voucher_repo: IVoucherRepo = VoucherRepo()
) -> list[ElasticSearchUserAffinityVoucher]:
    return voucher_repo.get_user_affinity_vouchers(request)


def get_unexpired_published_cba_voucher(
    voucher_repo: IVoucherRepo = VoucherRepo(),
) -> list[Voucher]:
    return voucher_repo.get_unexpired_published_cba_voucher()


def get_vouchers_by_ids(
    voucher_ids: list[str], voucher_repo: IVoucherRepo = VoucherRepo()
) -> list[Voucher]:
    return voucher_repo.get_by_ids(voucher_ids)


def get_top_vouchers(
    *,
    page: Page = TOP_VOUCHERS_DEFAULT_PAGE,
    order: Order = TOP_VOUCHERS_DEFAULT_ORDER,
    by_department: FriendlyId | None = None,
    by_departments: set[str] | None = None,
    by_category: FriendlyId | None = None,
    by_categories: set[str] | None = None,
    by_store: FriendlyId | None = None,
    by_stores: set[str] | None = None,
    by_brand: FriendlyId | None = None,
    by_brands: set[str] | None = None,
    by_coupon_types: list[str] | None = None,
    by_followed_user: str | None = None,
    department_repo: IDepartmentRepo = DepartmentRepo(),
    category_repo: ICategoryRepo = CategoryRepo(),
    store_repo: IStoreRepo = StoreRepo(),
    brand_repo: IBrandRepo = BrandRepo(),
    voucher_repo: IVoucherRepo = VoucherRepo(),
    user_repo: IUserRepo = UserRepo(),
) -> list[Voucher]:
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
    store_ids: set[str] = get_combined_entity_ids(by_store, by_stores, store_repo)
    brand_ids: set[str] = get_combined_entity_ids(by_brand, by_brands, brand_repo)

    if by_followed_user:
        # Filter by all store ids followed by this user
        if user_id := user_repo.get_id_by_friendly_id(by_followed_user):
            if followed_store_ids := store_repo.get_ids_followed_by_user_id(user_id):
                # Add followed store ids to the set if it already exists, else create new
                if store_ids:
                    store_ids.update(followed_store_ids)
                else:
                    store_ids = set(followed_store_ids)

    return voucher_repo.get_top_vouchers(
        page=page,
        order=order,
        department_id=department_id,
        department_ids=department_ids,
        category=category,
        category_ids=category_ids,
        store_ids=store_ids,
        brand_ids=brand_ids,
        coupon_types=by_coupon_types,
    )


def get_by_id_or_slug(
    identifier: FriendlyId, request: Request, voucher_repo: IVoucherRepo = VoucherRepo()
) -> Voucher | None:
    voucher = voucher_repo.get_by_id_or_slug(identifier)
    if voucher:
        voucher_repo.create_voucher_impression(
            voucher_id=voucher.id,
            user_id=request.context.user_id or 0,
            ip_address=request.context.client_ip,
            referrer=request.context.referrer,
        )
        return voucher
