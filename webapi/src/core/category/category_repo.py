"""
    This repository is related to Categories related DB Query
"""

from typing import Protocol

from psycopg2.extras import DictCursor, RealDictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.common.base_model import BaseModel
from src.core.category.entities import Category
from src.core.common.repository import FriendlyId


class CategoryRequest(BaseModel):
    by_department: int
    by_active: bool


class ICategoryRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface for categories repo
    """

    def get_by_friendly_id(self, friendly_id: FriendlyId) -> Category | None:
        """
        Get category id by id or slug
        """
        pass

    def get_categories(self, request: CategoryRequest) -> list[Category]:
        pass


class CategoryRepo(ICategoryRepo):  # pylint: disable=too-few-public-methods
    """
    CategoriesRepo class and related methods definition
    """

    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_by_friendly_id(self, friendly_id: FriendlyId) -> Category | None:
        query = f"""
            select 
                c.*
            from categories as c
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where c.id=%s
                    limit 1;
                """
            )
            values = [int(friendly_id)]
        else:
            query = (
                query
                + """
                    where c.slug=%s
                    limit 1;
                """
            )
            values = [friendly_id]
        result = self._rds_client.execute_fetch_one_query(
            query, values, cursor_factory=RealDictCursor
        )
        if result:
            return Category.model_validate(dict(result))
        else:
            return None

    def get_categories(self, request: CategoryRequest) -> list[Category]:
        results = self._rds_client.execute_fetch_all_query(
            self._get_categories_select_statement(),
            [request.by_department],
            DictCursor,
        )

        return [Category.model_validate(dict(category)) for category in results]

    @staticmethod
    def _get_categories_select_statement():
        select_fields = list(Category.__fields__.keys())
        select_statement = (
            f"SELECT {','.join(select_fields)} FROM categories "
            "where department_id=%s"
        )
        return select_statement
