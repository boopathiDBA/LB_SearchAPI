from src.core.department.department_repo import (
    IDepartmentRepo,
    DepartmentRepo,
    DepartmentRequest,
)
from src.core.department.entities import Department


def get_departments_by_filters(
    request: DepartmentRequest,
    department_repo: IDepartmentRepo = DepartmentRepo(),
) -> list[Department]:
    if request.by_followed:
        return department_repo.get_departments_followed_by(request.by_followed)
    else:
        return department_repo.get_departments()
