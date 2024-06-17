"""
This repository is related to Voucher Elasticsearch Queries
"""

import hashlib
import random
import time
from datetime import datetime, timedelta
from typing import Protocol

from psycopg2.extras import DictCursor, RealDictCursor

from src.adapters.elastic_search.elastic_search_client import (
    IElasticSearchClient,
    get_elastic_search_client,
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
from src.core.common.repository import Page, Order, OrderDirectionEnum, FriendlyId
from src.core.common.user_affinity.user_affinity_request import UserAffinityRequest
from src.core.voucher.entities import (
    ElasticSearchVoucher,
    ElasticSearchUserAffinityVoucher,
    Voucher,
    VoucherDBEntity,
)
from src.core.voucher.user_affinity_vouchers_search_elastic_processor import (
    UserAffinityVouchersSearchElasticProcessor,
)
from src.core.voucher.voucher_search_elastic_processor import (
    VoucherSearchElasticProcessor,
)


class IVoucherRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Elastic Search Voucher interface
    """

    def elastic_search(
        self, request: ElasticSearchRequest
    ) -> list[ElasticSearchVoucher]:
        """
        Elastic search for vouchers.
        """

    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        pass

    def get_user_affinity_vouchers(
        self, request: UserAffinityRequest
    ) -> list[ElasticSearchUserAffinityVoucher]:
        """Returns vouchers based on user's affinity."""
        pass

    def get_unexpired_published_cba_voucher(self) -> list[Voucher]:
        pass

    def get_by_ids(self, ids: list[str]) -> list[Voucher]:
        """Given a list of ids, return any Vouchers that match."""

    def get_by_id_or_slug(self, identifier: FriendlyId) -> Voucher | None:
        """
        Get voucher by store_id or slug.
        """

    def get_top_vouchers(
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
        coupon_types: list[str] | None,
    ) -> list[Voucher]:
        pass

    def create_voucher_impression(
        self,
        *,
        voucher_id: str,
        user_id: str,
        ip_address: str | None,
        referrer: str | None,
    ) -> None:
        """
        Create impression for voucher
        """


class VoucherRepo(IVoucherRepo):  # pylint: disable=too-few-public-methods
    """
    VoucherRepo class and related methods
    """

    def __init__(
        self,
        elastic_search_client: IElasticSearchClient = get_elastic_search_client(),
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._user_affinity_vouchers_processor = (
            UserAffinityVouchersSearchElasticProcessor()
        )
        self._voucher_search_elastic_processor = VoucherSearchElasticProcessor()
        self._elastic_search_client = elastic_search_client
        self._rds_client = rds_client

    def _create_request_hash(self) -> str:
        # Get the current timestamp as a float and convert it to a string
        timestamp = str(time.time())

        # Generate a random number and convert it to a string
        random_number = str(random.randint(0, 10000))

        # Concatenate the timestamp and random number
        data_to_hash = timestamp + random_number

        # Hash the concatenated string using SHA256
        hashed_data = hashlib.sha256(data_to_hash.encode()).hexdigest()

        return hashed_data

    def elastic_search(
        self, request: ElasticSearchRequest
    ) -> list[ElasticSearchVoucher]:
        vouchers_dict = self._voucher_search_elastic_processor.execute(
            self._elastic_search_client, request
        )

        return [ElasticSearchVoucher(**voucher) for voucher in vouchers_dict]

    def get_filter_options(
        self, request: ElasticSearchFilterOptionsRequest
    ) -> list[FilterOption]:
        return query_filter_options(request)

    def get_user_affinity_vouchers(
        self, request: UserAffinityRequest
    ) -> list[ElasticSearchUserAffinityVoucher]:
        results = self._user_affinity_vouchers_processor.execute(
            self._elastic_search_client, request
        )

        return [
            ElasticSearchUserAffinityVoucher.model_validate(result)
            for result in results
        ]

    def get_unexpired_published_cba_voucher(self) -> list[Voucher]:
        select_statement = (
            "SELECT c.*, s.name AS store_name "
            "FROM coupons AS c LEFT JOIN stores AS s ON s.id = c.store_id "
            "WHERE c.is_cba_exclusive=TRUE AND c.is_cba_icp=FALSE "
            "AND (c.expire_at=NULL OR c.expire_at>NOW()::timestamp) "
            "AND c.state='published';"
        )

        results = self._rds_client.execute_fetch_all_query(
            select_statement,
            [],
            DictCursor,
        )
        return [Voucher(**dict(voucher)) for voucher in results]

    def get_by_ids(self, ids: list[str]) -> list[Voucher]:
        if not ids:
            return []

        query = (
            "SELECT c.*, s.name AS store_name "
            "FROM coupons AS c LEFT JOIN stores AS s ON s.id = c.store_id "
            "WHERE c.id in %s"
        )

        results: list[dict] = self._rds_client.execute_fetch_all_query(
            query, [tuple(ids)], cursor_factory=RealDictCursor
        )

        return [Voucher.model_validate(dict(result)) for result in results]

    def _get_top_vouchers_query_select(self) -> str:
        select = f"""
            select 
                {', '.join([f'c.{k}' for k in VoucherDBEntity.model_fields.keys()])},
                tc.store_name as store_name,
                c.discount_amount AS offer
                from mv_top_coupons as tc
                join coupons as c
                    on c.id=tc.id
        """
        return select

    def _get_top_vouchers_query_filters(
        self,
        *,
        order: Order,
        department_id: str | None,
        department_ids: set[str] | None,
        category: Category | None,
        category_ids: set[str] | None,
        store_ids: set[str] | None,
        brand_ids: set[str] | None,
        coupon_types: list[str] | None,
        values: list,
    ) -> (str, list):
        two_days_ago = datetime.today() - timedelta(days=2)
        filters = ["c.expire_at IS NULL OR c.expire_at > %s"]
        values.append(two_days_ago)

        if department_id:
            filters.append(f"tc.department_id=%s")
            values.append(department_id)
            order.column = "department_rank"
            order.direction = OrderDirectionEnum.ASC
        if category:
            filters.append(f"tc.department_id=%s and tc.category_id in (%s, null)")
            values.extend([category.department_id, category.id])
            order.column = "category_rank"
            order.direction = OrderDirectionEnum.ASC
        if department_ids:
            filters.append(f"tc.department_id in %s")
            values.append(tuple(department_ids))
        if category_ids:
            filters.append(f"tc.category_id in %s")
            values.append(tuple(category_ids))
        if store_ids:
            filters.append(f"tc.store_id in %s")
            values.append(tuple(store_ids))
        if brand_ids:
            filters.append(f"tc.brand_id in %s")
            values.append(tuple(brand_ids))
        if coupon_types:
            filters.append(f"tc.coupon_type in %s")
            values.append(tuple(coupon_types))

        where = f"where {' and '.join(filters)}" if filters else ""
        return where, values

    def _get_top_vouchers_query_order(self, *, order: Order) -> str:
        order_by_column = (
            f"lower(tc.{order.column})"
            if order.column == "name"
            else f"tc.{order.column}"
        )
        order_by = f"""
            order by {order_by_column} {order.direction}
        """

        return order_by

    def _get_top_vouchers_query_and_values(
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
        coupon_types: list[str] | None,
    ) -> (str, list):
        values = []

        select = self._get_top_vouchers_query_select()

        where, values = self._get_top_vouchers_query_filters(
            order=order,
            department_id=department_id,
            department_ids=department_ids,
            category=category,
            category_ids=category_ids,
            store_ids=store_ids,
            brand_ids=brand_ids,
            coupon_types=coupon_types,
            values=values,
        )

        order_by = self._get_top_vouchers_query_order(order=order)

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

    def get_top_vouchers(
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
        coupon_types: list[str] | None,
    ) -> list[Voucher]:
        query, values = self._get_top_vouchers_query_and_values(
            page=page,
            order=order,
            department_id=department_id,
            department_ids=department_ids,
            category=category,
            category_ids=category_ids,
            store_ids=store_ids,
            brand_ids=brand_ids,
            coupon_types=coupon_types,
        )

        results = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Voucher.model_validate(dict(result)) for result in results]

    def get_by_id_or_slug(self, friendly_id: FriendlyId) -> Voucher | None:
        query = (
            "SELECT c.*, s.name as store_name FROM coupons AS c "
            "LEFT JOIN stores AS s ON s.id = c.store_id "
        )
        if friendly_id.strip().isdigit():
            query = query + "where c.id=%s; "
            friendly_id = int(friendly_id.strip())
        else:
            query = query + "where c.slug=%s; "

        result = self._rds_client.execute_fetch_one_query(
            query,
            [friendly_id],
            DictCursor,
        )
        if result:
            return Voucher(**dict(result))

    def create_voucher_impression(
        self,
        *,
        voucher_id: str,
        user_id: str,
        ip_address: str | None,
        referrer: str | None,
    ) -> None:
        query = """INSERT INTO impressions ( 
                        impressionable_type, impressionable_id, user_id, controller_name, 
                        action_name, request_hash, ip_address, referrer, created_at, updated_at
                        )
                    VALUES ('Coupon', %s, %s, 'coupons', 'show', %s, %s, %s, NOW(), NOW()
                    )
                 """

        self._rds_client.execute_insert_query(
            query,
            [voucher_id, user_id, self._create_request_hash(), ip_address, referrer],
        )
