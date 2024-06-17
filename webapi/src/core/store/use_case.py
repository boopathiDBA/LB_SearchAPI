from enum import StrEnum

from src.core.common.context import Context
from src.core.common.repository import (
    FriendlyId,
    Order,
    OrderDirectionEnum,
    Page,
    TOP_LIST_DEFAULT_PAGE,
)
from src.core.department.department_repo import IDepartmentRepo, DepartmentRepo
from src.core.store.entities import Store, TopStoreDBEntity
from src.core.store.store_repo import IStoreRepo, StoreRepo
from src.core.user.user_repo import IUserRepo, UserRepo

"""
All fields of TopStoreDBEntity are valid values for order_by[column] query param of top_lists/stores api
"""
TopStoresOrderColumnEnum = StrEnum(
    "TopStoresOrderColumnEnum", [*TopStoreDBEntity.model_fields]
)
TOP_STORES_DEFAULT_ORDER = Order(column="rank", direction=OrderDirectionEnum.ASC)


def get_store_by_friendly_id(
    friendly_id: FriendlyId,
    context: Context,
    store_repo: IStoreRepo = StoreRepo(),
) -> Store | None:
    return store_repo.get_store_by_friendly_id(friendly_id, context.user_id)


def get_stores_followed_by_user_id(
    user_id: str,
    store_repo: IStoreRepo = StoreRepo(),
) -> list[Store]:
    return store_repo.get_all_followed_by_user_id(user_id)


def get_top_stores(
    *,
    page: Page = TOP_LIST_DEFAULT_PAGE,
    order: Order = TOP_STORES_DEFAULT_ORDER,
    by_department: FriendlyId | None = None,
    by_followed_user: str | None = None,
    department_repo: IDepartmentRepo = DepartmentRepo(),
    store_repo: IStoreRepo = StoreRepo(),
    user_repo: IUserRepo = UserRepo(),
) -> list[Store]:
    department_id = (
        department_repo.get_id_by_friendly_id(by_department) if by_department else None
    )

    store_ids = set()
    if by_followed_user:
        # Filter by all store ids followed by this user
        if user_id := user_repo.get_id_by_friendly_id(by_followed_user):
            if followed_store_ids := store_repo.get_ids_followed_by_user_id(user_id):
                # Add followed store ids to the set if it already exists, else create new
                store_ids.update(followed_store_ids)

    return store_repo.get_top_stores(
        page=page,
        order=order,
        department_id=department_id,
        store_ids=store_ids,
    )
