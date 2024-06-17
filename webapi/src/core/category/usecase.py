from src.core.category.category_repo import (
    ICategoryRepo,
    CategoryRepo,
    CategoryRequest,
)
from src.core.category.entities import Category


def get_categories_by_filters(
    request: CategoryRequest,
    categories_repo: ICategoryRepo = CategoryRepo(),
) -> list[Category]:
    return categories_repo.get_categories(request)
