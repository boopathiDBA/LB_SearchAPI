from src.core.advertisement.advertisement_repo import (
    AdvertisementRepo,
    IAdvertisementRepo,
)
from src.core.common.repository import FriendlyId
from src.core.department.department_repo import DepartmentRepo, IDepartmentRepo
from src.core.category.category_repo import ICategoryRepo, CategoryRepo


def get_advertisements(
    *,
    by_page: FriendlyId | None,
    by_position: FriendlyId | None,
    by_list: FriendlyId | None,
    by_department: FriendlyId | None,
    by_category: FriendlyId | None,
    department_repo: IDepartmentRepo = DepartmentRepo(),
    category_repo: ICategoryRepo = CategoryRepo(),
    advertisement_repo: IAdvertisementRepo = AdvertisementRepo(),
):
    """Retrieve advertisements by filters.

    Currently `by_page`/`by_position`/`by_list` are TRUE filters where it is an AND functionality of the filter.
    However, for `by_department` and `by_category`, it is an OR functionality where if the values do not
    correspond to an actual entity (not found by id or slug) then the results will return as if the filter was not not given.
    """
    department_id = (
        department_repo.get_id_by_friendly_id(by_department) if by_department else None
    )

    if by_category and (category := category_repo.get_by_friendly_id(by_category)):
        category_id = category.id
    else:
        category_id = None

    return advertisement_repo.get_active_advertisements(
        by_page=by_page,
        by_position=by_position,
        by_list=by_list,
        department_id=department_id,
        category_id=category_id,
    )
