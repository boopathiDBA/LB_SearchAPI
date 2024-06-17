from enum import StrEnum

from src.core.brand.brand_repo import IBrandRepo, BrandRepo
from src.core.brand.entities import Brand
from src.core.common.context import Context
from src.core.common.repository import Page, Order, OrderDirectionEnum, FriendlyId
from src.core.department.department_repo import IDepartmentRepo, DepartmentRepo
from src.core.store.store_repo import IStoreRepo, StoreRepo


class TopBrandsOrderColumnEnum(StrEnum):
    NAME = "name"
    RANK = "rank"
    DEALS_COUNT = "deals_count"


TOP_BRANDS_DEFAULT_PAGE = Page(page_number=1, per_page=50)
TOP_BRANDS_DEFAULT_ORDER = Order(
    column=TopBrandsOrderColumnEnum.RANK, direction=OrderDirectionEnum.ASC
)


def get_brand_by_friendly_id(
    friendly_id: FriendlyId,
    context: Context,
    brand_repo: IBrandRepo = BrandRepo(),
) -> Brand | None:
    return brand_repo.get_by_friendly_id(friendly_id, context.user_id)


def get_brands_followed_by_user_id(
    user_id: str,
    brand_repo: IBrandRepo = BrandRepo(),
) -> list[Brand]:
    return brand_repo.get_all_followed_by_user_id(user_id)


def get_top_brands(
    *,
    page: Page = TOP_BRANDS_DEFAULT_PAGE,
    order: Order = TOP_BRANDS_DEFAULT_ORDER,
    context: Context,
    brand_repo: IBrandRepo = BrandRepo(),
) -> list[Brand]:
    return brand_repo.get_top_brands(
        page=page, order=order, current_user_id=context.user_id
    )


def get_top_brands_by_department(
    *,
    department_friendly_id: FriendlyId,
    page: Page = TOP_BRANDS_DEFAULT_PAGE,
    order: Order = TOP_BRANDS_DEFAULT_ORDER,
    context: Context,
    brand_repo: IBrandRepo = BrandRepo(),
    department_repo: IDepartmentRepo = DepartmentRepo(),
) -> list[Brand]:
    department_id = department_repo.get_id_by_friendly_id(department_friendly_id)
    return brand_repo.get_top_brands_by_department(
        department_id=department_id if department_id else None,
        page=page,
        order=order,
        current_user_id=context.user_id,
    )


def get_top_brands_by_store(
    *,
    store_friendly_id: FriendlyId,
    page: Page = TOP_BRANDS_DEFAULT_PAGE,
    order: Order = TOP_BRANDS_DEFAULT_ORDER,
    context: Context,
    brand_repo: IBrandRepo = BrandRepo(),
    store_repo: IStoreRepo = StoreRepo(),
) -> list[Brand]:
    store_id = store_repo.get_id_by_friendly_id(store_friendly_id)
    return brand_repo.get_top_brands_by_store(
        store_id=store_id if store_id else None,
        page=page,
        order=order,
        current_user_id=context.user_id,
    )


def get_top_brands_followed_by_user(
    *,
    user_id: str,
    page: Page = TOP_BRANDS_DEFAULT_PAGE,
    order: Order = TOP_BRANDS_DEFAULT_ORDER,
    brand_repo: IBrandRepo = BrandRepo(),
) -> list[Brand]:
    return brand_repo.get_top_brands_followed_by_user(
        user_id=user_id, page=page, order=order
    )
