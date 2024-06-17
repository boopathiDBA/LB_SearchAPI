from typing import Protocol
from psycopg2.extras import RealDictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.common.base_model import BaseModel
from src.core.custom_widget.entities import (
    CustomWidget,
    CustomWidgetPositionEnum,
)


class ICustomWidgetRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface for custom_widgets repo
    """

    def get_custom_widget(
        self, by_position: CustomWidgetPositionEnum
    ) -> CustomWidget | None:
        pass


class CustomWidgetRepo(ICustomWidgetRepo):  # pylint: disable=too-few-public-methods
    def __init__(self, rds_client: IRdsClient | None = None):
        self._rds_client = rds_client if rds_client else get_initialised_rds_client()

    def _filter_custom_widget_items(
        self, custom_widget_items: list[dict]
    ) -> list[dict]:
        return [
            item
            for item in custom_widget_items
            if item["item_id"] is not None and item["item_type"] is not None
        ]

    def get_custom_widget(
        self, by_position: CustomWidgetPositionEnum
    ) -> CustomWidget | None:
        """
        This method fetch only one CustomWidget based on position as required by the API
        """

        select_statement = """
            SELECT
                cw.*,
                json_agg(json_build_object(   'id',
                cwi.id,
                'item_type',
                cwi.item_type,
                'item_id',
                cwi.item_id,
                'position',
                cwi.position,
                'listing_url',
                cwi.listing_url,
                'sponsored',
                cwi.sponsored  )
                ORDER BY cwi.position
                ) AS items 
            FROM
                custom_widgets AS cw 
            LEFT JOIN
                custom_widget_items AS cwi 
                    ON cw.id = cwi.custom_widget_id 
            WHERE
                cw.position = %s  
                AND (
                    (
                        cw.start_date IS NOT NULL 
                        AND cw.start_date <= CURRENT_TIMESTAMP       
                        AND      (
                            cw.end_date IS NULL 
                            or cw.end_date > CURRENT_TIMESTAMP
                        )    
                    )   
                    OR (
                        cw.state = 'published' 
                        AND (
                            cw.end_date >= CURRENT_TIMESTAMP 
                            OR cw.end_date IS NULL
                        )
                    )   
                ) 
            GROUP BY
                cw.id;
        """

        result = self._rds_client.execute_fetch_one_query(
            select_statement,
            [by_position],
            RealDictCursor,
        )

        if not result:
            return None

        custom_widget_dict = dict(result)
        custom_widget_items = custom_widget_dict["items"]
        filtered_custom_widget_items = self._filter_custom_widget_items(
            custom_widget_items
        )

        return CustomWidget.model_validate(
            {**custom_widget_dict, "items": filtered_custom_widget_items}
        )
