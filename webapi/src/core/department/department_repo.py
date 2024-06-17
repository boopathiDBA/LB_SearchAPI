"""
    This repository is related to Departments related DB Query
"""

from typing import Protocol

from psycopg2.extras import DictCursor, RealDictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.common.base_model import BaseModel
from src.core.common.repository import FriendlyId
from src.core.department.entities import Department


class DepartmentRequest(BaseModel):
    by_followed: str | None = None


class IDepartmentRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface for departments repo
    """

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        """
        Get department id by id or slug
        """
        pass

    def get_departments(self) -> list[Department]:
        pass

    def get_departments_followed_by(self, user_id: str) -> list[Department]:
        pass


class DepartmentRepo(IDepartmentRepo):  # pylint: disable=too-few-public-methods
    """
    DepartmentsRepo class and related methods definition
    """

    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        query = f"""
            select 
                d.id
            from departments as d
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where d.id=%s
                    limit 1;
                """
            )
            values = [int(friendly_id)]
        else:
            query = (
                query
                + """
                    where d.slug=%s
                    limit 1;
                """
            )
            values = [friendly_id]
        result = self._rds_client.execute_fetch_one_query(
            query, values, cursor_factory=RealDictCursor
        )
        if result and "id" in dict(result):
            return str(dict(result).get("id", ""))
        else:
            return None

    def get_departments(self) -> list[Department]:
        select_statement = (
            f"SELECT d.*, array_agg(c.id) as category_ids FROM departments as d "
            "LEFT JOIN categories as c ON c.department_id = d.id "
            "GROUP BY d.id ;"
        )
        results = self._rds_client.execute_fetch_all_query(
            select_statement,
            [],
            DictCursor,
        )
        return [Department.model_validate(dict(result)) for result in results]

    def get_departments_followed_by(self, user_id: str):
        select_statement = (
            "SELECT d.*, array_agg(c.id) as category_ids FROM departments as d "
            "LEFT JOIN categories as c on c.department_id = d.id "
            "JOIN follows as f on f.followable_id = d.id "
            "WHERE f.followable_type = 'Department' and f.user_id=%s"
            "GROUP BY d.id;"
        )
        results = self._rds_client.execute_fetch_all_query(
            select_statement,
            [user_id],
            DictCursor,
        )
        return [Department.model_validate(dict(result)) for result in results]
