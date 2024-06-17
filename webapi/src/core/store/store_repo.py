import logging
from typing import Protocol

from psycopg2.extras import RealDictCursor

from src.adapters.rds_client import (
    IRdsClient,
    get_initialised_rds_client,
    RDSRequestException,
)
from src.core.common.repository import FriendlyId, Page, Order, OrderDirectionEnum
from src.core.store.entities import Store

logger = logging.getLogger(__name__)


class IStoreRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Elastic search Store interface
    """

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        """
        Get store id by id or slug
        """
        pass

    def get_store_by_friendly_id(
        self, friendly_id: FriendlyId, user_id: str | None = None
    ) -> Store | None:
        """
        Get store by store_id or slug.
        If user_id is present, user specific data like "followed" is added
        """

    def get_by_ids(self, store_ids: list[str]) -> list[Store]:
        """
        Get all stores from a list of store ids
        """

    def get_all_followed_by_user_id(self, user_id: str) -> list[Store]:
        """
        Get all stores followed by user_id
        """

    def get_ids_followed_by_user_id(self, user_id: str) -> list[str]:
        """
        Get all store ids followed by this user_id
        """

    def get_top_stores(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        store_ids: set[str] | None,
    ) -> list[Store]:
        pass


class StoreRepo(IStoreRepo):
    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        query = f"""
            select 
                s.id
            from stores as s
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where s.id=%s
                    limit 1;
                """
            )
            values = [int(friendly_id)]
        else:
            query = (
                query
                + """
                    where s.slug=%s
                    limit 1;
                """
            )
            values = [friendly_id]
        result = self._rds_client.execute_fetch_one_query(
            query, values, cursor_factory=RealDictCursor
        )
        if result and "id" in dict(result):
            return str(dict(result).get("id"))
        else:
            return None

    def get_store_by_friendly_id(
        self, friendly_id: FriendlyId, user_id: str | None = None
    ) -> Store | None:
        query = f"""
            select
                {', '.join([f's.{k}' for k in Store.model_fields.keys() if k not in ["followed", "store_rating", "store_reviews"]])},
                f.user_id is not null as followed,
                r.star_rating as store_rating,
                r.number_of_reviews as store_reviews
            from stores as s
            left join follows as f 
                on f.followable_id=s.id
                and f.followable_type='Store'
                and f.user_id=%s
            left join ratings as r
                on r.resource_type='Store'
                and r.resource_id=s.id
        """
        if friendly_id.strip().isdigit():
            query = (
                query
                + """
                    where s.id=%s
                    limit 1;
                """
            )
            values = [user_id, int(friendly_id.strip())]
        else:
            query = (
                query
                + """
                    where s.slug=%s
                    limit 1;
                """
            )
            values = [user_id, friendly_id.strip()]
        result: dict = self._rds_client.execute_fetch_one_query(
            query, values, cursor_factory=RealDictCursor
        )
        if result:
            return Store.model_validate(dict(result))
        else:
            return None

    def get_by_ids(self, store_ids: list[str]) -> list[Store]:
        if not store_ids:
            return []

        query = f"""
            select
                {', '.join([f's.{k}' for k in Store.model_fields.keys() if k not in ["followed", "store_rating", "store_reviews"]])},
                r.star_rating as store_rating,
                r.number_of_reviews as store_reviews
            from stores as s
            left join ratings as r
                on r.resource_type='Store'
                and r.resource_id=s.id
            where s.id in %s;
        """
        values = [tuple(store_ids)]
        results = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Store.model_validate(dict(result)) for result in results]

    def get_all_followed_by_user_id(self, user_id: str) -> list[Store]:
        query = f"""
            select
                {', '.join([f's.{k}' for k in Store.model_fields.keys() if k not in ["followed", "store_rating", "store_reviews"]])},
                true as followed,
                r.star_rating as store_rating,
                r.number_of_reviews as store_reviews
            from stores as s
            join follows as f
                on f.followable_id=s.id
                and f.followable_type='Store'
            left join ratings as r
                on r.resource_type='Store'
                and r.resource_id=s.id
            where f.user_id=%s;
        """
        values = [int(user_id)]
        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Store.model_validate(dict(result)) for result in results]

    def get_ids_followed_by_user_id(self, user_id: str) -> list[str]:
        query = f"""
            select
                f.followable_id as id
            from follows as f
            where
                f.followable_type='Store'
                and f.user_id=%s;
        """
        values = [int(user_id)]
        results = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [str(dict(result).get("id")) for result in results]

    def _get_top_stores_query_and_values(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        store_ids: set[str] | None,
    ) -> (str, list):
        values = []

        select = f"""
            select
                {', '.join([f's.{k}' for k in Store.model_fields.keys() if k not in ["followed", "store_rating", "store_reviews"]])},
                r.star_rating as store_rating,
                r.number_of_reviews as store_reviews
            from mv_top_stores as ts
                join stores as s
                    on s.id=ts.id
            left join ratings as r
                on r.resource_type='Store'
                and r.resource_id=s.id
        """

        filters = []
        if department_id:
            filters.append(
                f"ts.d_{department_id}_score > 0 OR ts.fixed_d_{department_id}_score > 0"
            )
            order.column = f"d_{department_id}_rank"
            order.direction = OrderDirectionEnum.ASC

        if store_ids:
            filters.append(f"ts.id in %s")
            values.append(tuple(store_ids))

        where = f"where {' and '.join(filters)}" if filters else ""

        order_by_column = (
            f"lower(ts.{order.column})"
            if order.column == "name"
            else f"ts.{order.column}"
        )
        order_by = f"order by {order_by_column} {order.direction}"

        limit = f"limit {page.per_page}"
        offset = f"offset {(page.page_number - 1) * page.per_page}"

        query = f"""
            {select}
            {where}
            {order_by}
            {limit}
            {offset}
        """
        return query, values

    def get_top_stores(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        store_ids: set[str] | None,
    ) -> list[Store]:
        query, values = self._get_top_stores_query_and_values(
            page=page,
            order=order,
            department_id=department_id,
            store_ids=store_ids,
        )

        """
        This flow queries the materialized view mv_top_stores.
        This view has individual columns defined for each of the department.
        e.g If argument `department_id` == 86, this will query the column `d_86_score` and `fixed_d_86_score`
        Currently there is no automated process to update the columns in the materialized view
            when departments data is added/updated.
        Therefore, this query can throw error if it encounters any new/unknown department column.
        Currently, we are handling it by catching the error and returning empty results.
        An alternate way to handle would be to check for the existence of the column in the query itself.
            Ref - https://gist.github.com/drawcode/4441656
        """
        try:
            results = self._rds_client.execute_fetch_all_query(
                query, values, cursor_factory=RealDictCursor
            )
        except RDSRequestException as e:
            if "column" in str(e) and "does not exist" in str(e):
                logger.error(e)
                results = []
            else:
                raise e

        return [Store.model_validate(dict(result)) for result in results]
