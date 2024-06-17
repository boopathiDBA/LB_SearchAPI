"""
    This repository is related to Upvoted Voucher related DB Query
"""

from enum import StrEnum
from typing import Protocol

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client


class VotableTypeEnum(StrEnum):
    """Supported Votable types."""

    VOUCHER = "Coupon"
    SALE_EVENT = "SaleEvent"


class IVotesRepo(Protocol):  # pylint: disable=too-few-public-methods
    """
    Interface for votes repo
    """

    def get_votable_ids_for_user(
        self, user_id: str, votable_type: VotableTypeEnum
    ) -> list[str]:
        """
        Get user's upvoted vouchers
        """


class VotesRepo(IVotesRepo):  # pylint: disable=too-few-public-methods
    """
    VotesRepo class and related methods definition
    """

    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def get_votable_ids_for_user(
        self, user_id: str, votable_type: VotableTypeEnum
    ) -> list[str]:
        votable_ids = []
        select_statement = (
            "SELECT votable_id FROM votes where votable_type=%s and user_id=%s"
        )
        results = self._rds_client.execute_fetch_all_query(
            select_statement, [votable_type, user_id]
        )
        votable_ids = [str(votable_id) for (votable_id,) in results]
        return votable_ids
