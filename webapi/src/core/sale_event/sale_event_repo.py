"""
This repository is related to SaleEvent Elasticsearch Queries
"""

from typing import Protocol

from psycopg2.extras import DictCursor, RealDictCursor

from src.adapters.elastic_search.elastic_search_client import (
    get_elastic_search_client,
    IElasticSearchClient,
)
from src.adapters.elastic_search.queries.filter_options import (
    ElasticSearchFilterOptionsRequest,
    query_filter_options,
    FilterOption,
)
from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.core.category.entities import Category
from src.core.common.elastic_search.search_elastic_processor_base import (
    ElasticSearchRequest,
)
from src.core.common.repository import Page, Order, OrderDirectionEnum
from src.core.common.user_affinity.user_affinity_request import UserAffinityRequest
from src.core.sale_event.entities import (
    ElasticSearchSaleEvent,
    ElasticSearchUserAffinitySaleEvent,
)
from src.core.sale_event.entities import SaleEvent
from src.core.sale_event.sale_event_search_elastic_processor import (
    SaleEventSearchElasticProcessor,
)
from src.core.sale_event.user_affinity_sale_events_elastic_search_processor import (
    UserAffinitySaleEventsElasticSearchProcessor,
)


class ISaleEventRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    ElasticSearch SaleEvent interface
    """

    def elastic_search(
        self, request: ElasticSearchRequest
    ) -> list[ElasticSearchSaleEvent]:
        """
        Elastic search for sale_events.
        """

    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        pass

    def get_user_affinity_sale_events(
        self, request: UserAffinityRequest
    ) -> list[ElasticSearchUserAffinitySaleEvent]:
        """Returns sale events based on user's affinity."""
        pass

    def get_unexpired_published_cba_sale_event(self) -> list[SaleEvent]:
        pass

    def get_top_sale_events(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        department_ids: set[str] | None,
        category: Category | None,
        category_ids: set[str] | None,
        store_ids: set[str] | None,
        brand_ids: set[str] | None,
        current: bool | None,
        upcoming: bool | None,
    ) -> list[SaleEvent]:
        pass

    def get_by_ids(self, ids: list[str]) -> list[SaleEvent]:
        """Given a list of ids, return any SaleEvents that match."""
        pass


class SaleEventRepo(ISaleEventRepo):  # pylint: disable=too-few-public-methods
    """
    SaleEventRepo class and related methods
    """

    def __init__(
        self,
        elastic_search_client: IElasticSearchClient = get_elastic_search_client(),
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._user_affinity_sale_event_processor = (
            UserAffinitySaleEventsElasticSearchProcessor()
        )
        self._sale_event_search_elastic_processor = SaleEventSearchElasticProcessor()
        self._elastic_search_client = elastic_search_client
        self._rds_client = rds_client

    def elastic_search(
        self, request: ElasticSearchRequest
    ) -> list[ElasticSearchSaleEvent]:
        sale_event_dict = self._sale_event_search_elastic_processor.execute(
            self._elastic_search_client, request
        )

        return [ElasticSearchSaleEvent(**sale_event) for sale_event in sale_event_dict]

    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        return query_filter_options(request)

    def get_user_affinity_sale_events(
        self, request: UserAffinityRequest
    ) -> list[ElasticSearchUserAffinitySaleEvent]:
        results = self._user_affinity_sale_event_processor.execute(
            self._elastic_search_client, request
        )

        return [
            ElasticSearchUserAffinitySaleEvent.model_validate(result)
            for result in results
        ]

    def get_unexpired_published_cba_sale_event(self) -> list[SaleEvent]:
        select_statement = (
            "SELECT se.*, s.name as store_name "
            "FROM sale_events AS se LEFT JOIN stores AS s ON s.id = se.store_id "
            "WHERE se.is_cba_exclusive=TRUE AND se.expire_at>NOW()::timestamp "
            "AND se.state='published';"
        )
        results = self._rds_client.execute_fetch_all_query(
            select_statement,
            [],
            DictCursor,
        )
        return [SaleEvent(**dict(event)) for event in results]

    def _get_top_sale_events_query_order_and_limit(
        self, *, page: Page, order: Order, values: list
    ) -> (str, str, str, list):
        order_by_column = (
            f"lower(tse.{order.column})"
            if order.column == "name"
            else f"tse.{order.column}"
        )
        order_by = f"""
            order by {order_by_column} {order.direction}
        """

        limit = f"limit {page.per_page}"
        offset = f"offset {(page.page_number - 1) * page.per_page}"

        return order_by, limit, offset, values

    def _get_top_sale_events_query_filters(
        self,
        *,
        order: Order,
        department_id: str | None,
        department_ids: set[str] | None,
        category: Category | None,
        category_ids: set[str] | None,
        store_ids: set[str] | None,
        brand_ids: set[str] | None,
        current: bool | None,
        upcoming: bool | None,
        values: list,
    ) -> (str, list):
        filters = ["tse.expire_at IS NULL OR tse.expire_at > NOW()"]

        if department_id:
            filters.append(f"tse.department_id=%s")
            values.append(department_id)
            order.column = "department_rank"
            order.direction = OrderDirectionEnum.ASC
        if category:
            filters.append(f"tse.department_id=%s and tse.category_id in (%s, null)")
            values.extend([category.department_id, category.id])
            order.column = "category_rank"
            order.direction = OrderDirectionEnum.ASC
        if department_ids:
            filters.append(f"tse.department_id in %s")
            values.append(tuple(department_ids))
        if category_ids:
            filters.append(f"tse.category_id in %s")
            values.append(tuple(category_ids))
        if store_ids:
            filters.append(f"tse.store_id in %s")
            values.append(tuple(store_ids))
        if brand_ids:
            filters.append(f"tse.brand_id in %s")
            values.append(tuple(brand_ids))
        if upcoming:
            filters.append(f"NOW() < tse.start_at")
        if current:
            filters.append(f"NOW() BETWEEN tse.start_at AND tse.expire_at")

        where = f"where {' and '.join(filters)}" if filters else ""
        return where, values

    def _get_top_sale_events_query_select(self) -> str:
        select = f"""
            select 
                se.*, tse.store_name as store_name
                from mv_top_sale_events as tse
                join sale_events as se
                    on se.id=tse.id
        """
        return select

    def _get_top_sale_events_query_and_values(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        department_ids: set[str] | None,
        category: Category | None,
        category_ids: set[str] | None,
        store_ids: set[str] | None,
        brand_ids: set[str] | None,
        current: bool | None,
        upcoming: bool | None,
    ) -> (str, list):
        values = []
        select = self._get_top_sale_events_query_select()

        where, values = self._get_top_sale_events_query_filters(
            order=order,
            department_id=department_id,
            department_ids=department_ids,
            category=category,
            category_ids=category_ids,
            store_ids=store_ids,
            brand_ids=brand_ids,
            current=current,
            upcoming=upcoming,
            values=values,
        )
        (
            order_by,
            limit,
            offset,
            values,
        ) = self._get_top_sale_events_query_order_and_limit(
            page=page, order=order, values=values
        )

        query = f"""
            {select}
            {where}
            {order_by}
            {limit}
            {offset}
        """
        return query, values

    def get_top_sale_events(
        self,
        *,
        page: Page,
        order: Order,
        department_id: str | None,
        department_ids: set[str] | None,
        category: Category | None,
        category_ids: set[str] | None,
        store_ids: set[str] | None,
        brand_ids: set[str] | None,
        current: bool | None,
        upcoming: bool | None,
    ) -> list[SaleEvent]:
        query, values = self._get_top_sale_events_query_and_values(
            page=page,
            order=order,
            department_id=department_id,
            department_ids=department_ids,
            category=category,
            category_ids=category_ids,
            store_ids=store_ids,
            brand_ids=brand_ids,
            current=current,
            upcoming=upcoming,
        )

        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [SaleEvent.model_validate(dict(result)) for result in results]

    def get_by_ids(self, ids: list[str]) -> list[SaleEvent]:
        if not ids:
            return []

        query = (
            "SELECT se.*, s.name as store_name "
            "FROM sale_events AS se LEFT JOIN stores AS s ON s.id = se.store_id "
            "WHERE se.id in %s"
        )

        results = self._rds_client.execute_fetch_all_query(
            query, [tuple(ids)], cursor_factory=RealDictCursor
        )

        return [SaleEvent.model_validate(dict(result)) for result in results]
