"""
    This repository is related to Users related DB Query
"""

from typing import Protocol

from psycopg2.extras import DictCursor, RealDictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.core.common.repository import FriendlyId
from src.core.user.entities import User, UserNotificationSetting


class IUserRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface for users repo
    """

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        """
        Get user id by id or slug
        """
        pass

    def get_user_by_id(self, user_id: str) -> User | None:
        pass

    def get_user_wtid(self, user_id: str) -> str | None:
        pass


class UserRepo(IUserRepo):  # pylint: disable=too-few-public-methods
    """
    UsersRepo class and related methods definition
    """

    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_id_by_friendly_id(self, friendly_id: FriendlyId) -> str | None:
        query = f"""
            select 
                u.id
            from users as u
        """
        if friendly_id.isdigit():
            query = (
                query
                + """
                    where u.id=%s
                    limit 1;
                """
            )
            values = [int(friendly_id)]
        else:
            query = (
                query
                + """
                    where u.slug=%s
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

    def _get_users_by_id_sql_statement(self) -> str:
        # Mapping of field names to column names
        notif_field_to_column_map = {
            "global_": "global",
        }

        notif_columns_list = [
            notif_field_to_column_map.get(field_name, field_name)
            for field_name in UserNotificationSetting.model_fields.keys()
        ]
        json_build_statement = ", ".join([f"'{u}', n.{u}" for u in notif_columns_list])

        return f"""
            select u.*,
                json_build_object({json_build_statement}) as notification_setting,
                'Brand'=ANY(ARRAY_AGG(DISTINCT f.followable_type)) as brand_followed,
                'Department'=ANY(ARRAY_AGG(DISTINCT f.followable_type)) as department_followed,
                'Store'=ANY(ARRAY_AGG(DISTINCT f.followable_type)) as store_followed
            from users as u
                join notification_settings as n
                    on u.id = n.user_id
                left join follows as f
                    on f.user_id = u.id
            where u.id=%s
            group by u.id, n.id
        """

    def get_user_by_id(self, user_id: str) -> User | None:
        result = self._rds_client.execute_fetch_one_query(
            self._get_users_by_id_sql_statement(),
            [user_id],
            DictCursor,
        )
        if result:
            result_dict = dict(result)
            user = User.model_validate(
                {
                    **result_dict,
                }
            )

            return user
        else:
            return None

    def get_user_wtid(self, user_id: str) -> str | None:
        result = self._rds_client.execute_fetch_one_query(
            "select wtid from user_parameters where user_id = %s",
            [user_id],
            DictCursor,
        )

        return dict(result)["wtid"]
