import logging
from typing import Protocol

from psycopg2.extras import RealDictCursor

from src.adapters.rds_client import (
    IRdsClient,
    get_initialised_rds_client,
    RDSRequestException,
)
from src.core.brand.entities import Brand
from src.core.common.repository import Page, Order, OrderDirectionEnum, FriendlyId

logger = logging.getLogger(__name__)


class IBrandRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Elastic search Brand interface
    """

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        """
        Get brand id by id or slug
        """
        pass

    def get_by_friendly_id(
        self, friendly_id: FriendlyId, user_id: str | None
    ) -> Brand | None:
        """
        Get brand by brand_id or slug.
        If user_id is present, user specific data like "followed" is added
        """

    def get_all_followed_by_user_id(self, user_id: str) -> list[Brand]:
        """
        Get brands followed by user_id.
        """

    def get_top_brands(
        self, *, page: Page, order: Order, current_user_id: str | None
    ) -> list[Brand]:
        """
        Get top brands list by page and order
        If current_user_id is present, user specific data like "followed" is added
        """

    def get_top_brands_followed_by_user(
        self, *, user_id: str, page: Page, order: Order
    ) -> list[Brand]:
        """
        Get top brands list followed by the user: user_id
        """

    def get_top_brands_by_department(
        self,
        *,
        department_id: str | None,
        page: Page,
        order: Order,
        current_user_id: str | None,
    ) -> list[Brand]:
        """
        Get top brands list for the given department
        If current_user_id is present, user specific data like "followed" is added
        If department_id is None, it will behave like get_top_brands()
        """

    def get_top_brands_by_store(
        self,
        *,
        store_id: str | None,
        page: Page,
        order: Order,
        current_user_id: str | None,
    ) -> list[Brand]:
        """
        Get top brands list for the given store
        If current_user_id is present, user specific data like "followed" is added
        If store_id is None, it will behave like get_top_brands()
        """


class BrandRepo(IBrandRepo):
    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        query = f"""
            select 
                b.id
            from brands as b
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where b.id=%s
                    limit 1;
                """
            )
            values = [int(friendly_id)]
        else:
            query = (
                query
                + """
                    where b.slug=%s
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

    def get_by_friendly_id(
        self, friendly_id: FriendlyId, user_id: str | None
    ) -> Brand | None:
        query = f"""
            select 
                {', '.join([f'b.{k}' for k in Brand.model_fields.keys() if k != 'followed'])},
                f.user_id is not null as followed
            from brands as b
            left join follows as f 
                on f.followable_id=b.id
                and f.followable_type='Brand'
                and f.user_id=%s
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where b.id=%s
                    limit 1;
                """
            )
            values = [user_id, int(friendly_id)]
        else:
            query = (
                query
                + """
                    where b.slug=%s
                    limit 1;
                """
            )
            values = [user_id, friendly_id]
        result = self._rds_client.execute_fetch_one_query(
            query, values, cursor_factory=RealDictCursor
        )
        if result:
            return Brand.model_validate(dict(result))
        else:
            return None

    def get_all_followed_by_user_id(self, user_id: str) -> list[Brand]:
        query = f"""
            select 
                {', '.join([f'b.{k}' for k in Brand.model_fields.keys() if k != 'followed'])},
                true as followed
            from brands as b
            join follows as f 
                on f.followable_id=b.id
                and f.followable_type='Brand'
            where f.user_id=%s;
        """
        values = [int(user_id)]
        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Brand.model_validate(dict(result)) for result in results]

    def _get_top_brands_query_and_values(
        self,
        *,
        page: Page,
        order: Order,
        user_id: str | None = None,
        department_id: str | None = None,
        store_id: str | None = None,
        strict_follow_filter: bool = False,
    ) -> (str, list[str]):
        values = []
        select = (
            f"""
            select 
                {', '.join([f'b.{k}' for k in Brand.model_fields.keys() if k != 'followed'])},
                f.user_id is not null as followed
                from mv_top_brands as tb
        """
            if not store_id
            else f"""
            select 
                {', '.join([f'b.{k}' for k in Brand.model_fields.keys() if k != 'followed'])},
                f.user_id is not null as followed
                from mv_top_deals_kafka as tdk
        """
        )

        join = f"""
            join brands as b
                on b.id=tb.id
            {"join" if strict_follow_filter else "left join"} follows as f
                on f.followable_id=b.id
                and f.followable_type='Brand'
                and f.user_id=%s
        """
        if store_id:
            join = (
                f"""
                join mv_top_brands as tb
                    on tdk.brand_id=tb.id
            """
                + join
            )
        values.append(user_id)

        if department_id:
            where = f"where d_{department_id}_score > 0 or fixed_d_{department_id}_score > 0"
        elif store_id:
            where = f"where tdk.store_id={store_id} and tdk.brand_id is not null"
        else:
            where = ""

        if department_id:
            order.column = f"d_{department_id}_rank"
            order.direction = OrderDirectionEnum.ASC

        order_by_column = (
            f"lower(tb.{order.column})"
            if order.column == "name"
            else f"tb.{order.column}"
        )
        order_by = f"""
            order by {order_by_column} {order.direction}
        """

        group_by = f"group by b.id, f.user_id, {order_by_column}" if store_id else ""

        limit = f"limit {page.per_page}"
        offset = f"offset {(page.page_number - 1) * page.per_page}"

        query = f"""
            {select}
            {join}
            {where}
            {group_by}
            {order_by}
            {limit}
            {offset}
        """

        return query, values

    def get_top_brands(
        self, *, page: Page, order: Order, current_user_id: str | None
    ) -> list[Brand]:
        query, values = self._get_top_brands_query_and_values(
            page=page, order=order, user_id=current_user_id, strict_follow_filter=False
        )

        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Brand.model_validate(dict(result)) for result in results]

    def get_top_brands_followed_by_user(
        self, *, user_id: str, page: Page, order: Order
    ) -> list[Brand]:
        query, values = self._get_top_brands_query_and_values(
            page=page, order=order, user_id=user_id, strict_follow_filter=True
        )

        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Brand.model_validate(dict(result)) for result in results]

    def get_top_brands_by_department(
        self,
        *,
        department_id: str | None,
        page: Page,
        order: Order,
        current_user_id: str | None,
    ) -> list[Brand]:
        query, values = self._get_top_brands_query_and_values(
            page=page,
            order=order,
            user_id=current_user_id,
            department_id=department_id,
            strict_follow_filter=False,
        )

        """
        This flow queries the materialized view mv_top_brands.
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
        return [Brand.model_validate(dict(result)) for result in results]

    def get_top_brands_by_store(
        self,
        *,
        store_id: str | None,
        page: Page,
        order: Order,
        current_user_id: str | None,
    ) -> list[Brand]:
        query, values = self._get_top_brands_query_and_values(
            page=page,
            order=order,
            user_id=current_user_id,
            store_id=store_id,
            strict_follow_filter=False,
        )

        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Brand.model_validate(dict(result)) for result in results]
