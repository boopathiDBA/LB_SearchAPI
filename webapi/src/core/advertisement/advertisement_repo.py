from typing import Protocol

from psycopg2.extras import RealDictCursor

from src.core.advertisement.entities import Advertisement
from src.core.common.repository import FriendlyId
from src.adapters.rds_client import IRdsClient, get_initialised_rds_client


class IAdvertisementRepo(Protocol):  # pylint: disable=too-few-public-methods
    def get_active_advertisements(
        self,
        *,
        by_page: FriendlyId | None,
        by_position: FriendlyId | None,
        by_list: FriendlyId | None,
        department_id: str | None,
        category_id: str | None,
    ) -> list[Advertisement]:
        """
        Return list of active advertisements by filters.

        Advertisement is considered 'active' if the current date is between the start and end date of the advertisement.
        """
        pass


class AdvertisementRepo(IAdvertisementRepo):  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        rds_client: IRdsClient = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def _get_advertisements_sql_select(self) -> str:
        """Return the select statement for advertisements."""
        advertisement_columns = Advertisement.model_fields.keys()
        return f"select distinct {', '.join([f'a.{k}' for k in advertisement_columns])}"

    def _get_advertisements_sql_joins(self) -> str:
        return """
            JOIN ad_placements ap ON a.id = ap.advertisement_id
            JOIN ad_locations al ON ap.ad_location_id = al.id
        """

    def _get_advertisements_sql_where(
        self,
        *,
        values: list[str | int],
        by_page: FriendlyId | None,
        by_position: FriendlyId | None,
        by_list: FriendlyId | None,
        department_id: str | None,
        category_id: str | None,
    ) -> tuple[str, list[str | int]]:
        # Only return Advertisements that are active
        where_statement = "WHERE a.start_date <= CURRENT_TIMESTAMP AND a.end_date >= CURRENT_TIMESTAMP"
        if by_page:
            where_statement += " AND al.page = %s"
            values.append(by_page)
        if by_position:
            # Note: The column in ad_locations table is named `placement` not `position`
            where_statement += " AND al.placement = %s"
            values.append(by_position)
        if by_list:
            where_statement += " AND al.list = %s"
            values.append(by_list)
        if department_id:
            where_statement += " AND al.department_id = %s"
            values.append(department_id)
        if category_id:
            where_statement += " AND al.category_id = %s"
            values.append(category_id)

        return where_statement, values

    def _get_advertisements_query_values(
        self,
        *,
        by_page: FriendlyId | None,
        by_position: FriendlyId | None,
        by_list: FriendlyId | None,
        department_id: str | None,
        category_id: str | None,
    ) -> tuple[str, list[str | int]]:
        values = []
        select = self._get_advertisements_sql_select()
        joins = self._get_advertisements_sql_joins()
        where, values = self._get_advertisements_sql_where(
            values=values,
            by_page=by_page,
            by_position=by_position,
            by_list=by_list,
            department_id=department_id,
            category_id=category_id,
        )
        limit = "limit 3"

        query = f"""
            {select}
            from advertisements as a
            {joins}
            {where}
            {limit}
        """

        return query, values

    def get_active_advertisements(
        self,
        *,
        by_page: FriendlyId | None,
        by_position: FriendlyId | None,
        by_list: FriendlyId | None,
        department_id: str | None,
        category_id: str | None,
    ) -> list[Advertisement]:
        query, values = self._get_advertisements_query_values(
            by_page=by_page,
            by_position=by_position,
            by_list=by_list,
            department_id=department_id,
            category_id=category_id,
        )

        results = self._rds_client.execute_fetch_all_query(
            query, values, cursor_factory=RealDictCursor
        )
        return [Advertisement.model_validate(dict(result)) for result in results]
