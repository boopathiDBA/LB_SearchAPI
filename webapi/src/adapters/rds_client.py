import logging
import os
from typing import Protocol, TypeAlias, Type

import psycopg2
from psycopg2._psycopg import cursor as CursorFactory

logger = logging.getLogger(__name__)

PsycopgConnection: TypeAlias = any
PsycopgCursor: TypeAlias = any


class RDSRequestException(Exception):
    pass


class IRdsClient(Protocol):
    def execute_fetch_all_query(
        self,
        query_statement: str,
        parameters: list,
        cursor_factory: Type[CursorFactory] = None,
    ) -> list[tuple[any, ...]] | list[dict[any, any]] | None:
        pass

    def execute_fetch_one_query(
        self,
        query_statement: str,
        parameters: list,
        cursor_factory: Type[CursorFactory] = None,
    ) -> tuple[any, ...] | dict[any, any] | None:
        pass

    def execute_insert_query(self, query_statement: str, parameters: list) -> None:
        pass


class RdsClient(IRdsClient):
    def __init__(
        self, rds_host: str, rds_database: str, rds_user: str, rds_password: str
    ):
        self._rds_host = rds_host
        self._rds_database = rds_database
        self._rds_user = rds_user
        self._rds_password = rds_password

        # Accessing this variable is unsafe. Use the method _get_db_connection() instead.
        self._unsafe_db_connection: PsycopgConnection | None = None

    def initialise_db_connection(self) -> None:
        """Initialise db connection ensuring that a connection is made to db."""
        self._get_db_connection()

    def execute_fetch_all_query(
        self,
        query_statement: str,
        parameters: list,
        cursor_factory: Type[CursorFactory] = None,
    ) -> list[tuple[any, ...]] | list[dict[any, any]] | None:
        try:
            with self._get_cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query_statement, parameters)
                result = cur.fetchall()
                return result
        except (Exception, psycopg2.Error) as e:
            raise RDSRequestException(str(e))

    def execute_fetch_one_query(
        self,
        query_statement: str,
        parameters: list,
        cursor_factory: Type[CursorFactory] = None,
    ) -> tuple[any, ...] | dict[any, any] | None:
        try:
            with self._get_cursor(cursor_factory=cursor_factory) as cur:
                cur.execute(query_statement, parameters)
                result = cur.fetchone()
                return result
        except (Exception, psycopg2.Error) as e:
            raise RDSRequestException(str(e))

    def execute_insert_query(self, query_statement: str, parameters: list) -> None:
        try:
            connection = self._get_db_connection()

            with self._get_cursor() as cur:
                cur.execute(query_statement, parameters)
                connection.commit()
        except (Exception, psycopg2.Error) as e:
            raise RDSRequestException(str(e))

    def _get_db_connection(self) -> PsycopgConnection:
        """Return existing db connection. If one doesn't exist, create a new one."""
        if self._unsafe_db_connection is None:
            self._unsafe_db_connection = self._get_new_db_connection()
        return self._unsafe_db_connection

    def _get_cursor(self, cursor_factory: Type[CursorFactory] = None) -> PsycopgCursor:
        """Return a cursor for the current db connection.

        If the connection is invalid, reconnect and return a new cursor."""

        connection = self._get_db_connection()
        cursor = None
        try:
            cursor = (
                connection.cursor(cursor_factory=cursor_factory)
                if cursor_factory
                else connection.cursor()
            )
        # Handle psycopg2.InterfaceError: connection already closed
        except psycopg2.InterfaceError as e:
            if connection and cursor:
                cursor.close()

            self._reconnect_db()
            cursor = self._get_db_connection().cursor()

        return cursor

    def _reconnect_db(self):
        if self._unsafe_db_connection:
            self._unsafe_db_connection.close()

        self._unsafe_db_connection = None
        self._unsafe_db_connection = self._get_new_db_connection()

    def _get_new_db_connection(self):
        conn = psycopg2.connect(
            host=self._rds_host,
            database=self._rds_database,
            user=self._rds_user,
            password=self._rds_password,
            connect_timeout=10,
        )
        """
        Note: By default, any query execution, including a simple SELECT will
        start a transaction: for long-running programs, if no further action 
        is taken, the session will remain “idle in transaction”, an undesirable 
        condition for several reasons (locks are held by the session, tables bloat…).
        For long lived scripts, either ensure to terminate a transaction as soon 
        as possible or use an autocommit connection.

        By default autocmommit is False. Which means that transactions are auto
        created by default, therefore it is needed to explicitly commit after each
        cursor call.

        source: https://www.psycopg.org/docs/connection.html

        Set to True to ensure each query is auto committed.

        The consequence of this is that transactions now need to be created explicitly.
        Currently there is no need for database transactions, so setting to True is 
        simplier and safer for now.
        """
        conn.autocommit = True

        return conn


_SINGLETON_RDS_CLIENT: IRdsClient | None = None


def get_initialised_rds_client() -> IRdsClient:
    """Return an instance of RdsClient.
    Currently, this ensures only one instance is always return aka Singleton Pattern."""

    global _SINGLETON_RDS_CLIENT
    if _SINGLETON_RDS_CLIENT:
        return _SINGLETON_RDS_CLIENT
    else:
        rds_host = os.getenv("DATABASE_URL", "dbw.web.littlebirdie.dev")
        rds_database = os.getenv("DATABASE_DBNAME", "project-deals-staging")
        rds_user = os.getenv("DATABASE_USER", "postgres")
        rds_password = os.getenv("DATABASE_PASSWORD", "")

        _SINGLETON_RDS_CLIENT = RdsClient(
            rds_host, rds_database, rds_user, rds_password
        )

        # Connect to db during application start up to ensure first request already has existing connection.
        _SINGLETON_RDS_CLIENT.initialise_db_connection()

        return _SINGLETON_RDS_CLIENT
