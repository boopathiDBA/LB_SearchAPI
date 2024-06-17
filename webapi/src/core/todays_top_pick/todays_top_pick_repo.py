from typing import Protocol
from psycopg2.extras import RealDictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.core.todays_top_pick.entities import TodaysTopPick


class ITodaysTopPickRepo(Protocol):
    def get_todays_top_picks(self) -> list[TodaysTopPick]:
        """Return all non empty Today top picks.

        Empty Top picks are non returned, which are defined as rows without featurable_id configured

        Currently there are a maximum 50 rows in the table.

        There can be existing empty rows as the business may only configure a subset of rows instead of all 50.
        """
        pass


class TodaysTopPickRepo(ITodaysTopPickRepo):
    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_todays_top_picks(self) -> list[TodaysTopPick]:
        # Some rows may be empty without featurables configured, so we filter them out
        query = "SELECT * FROM todays_top_picks WHERE featurable_id IS NOT NULL"
        results = self._rds_client.execute_fetch_all_query(
            query, [], cursor_factory=RealDictCursor
        )

        if results is None:
            return []
        else:
            return [TodaysTopPick.model_validate(dict(result)) for result in results]
