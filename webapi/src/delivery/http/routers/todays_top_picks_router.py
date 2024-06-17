from collections import defaultdict
from enum import StrEnum
from typing import Annotated, TypeAlias
from fastapi import APIRouter, Depends

from src.common.string_utils import pascal_case_to_snake_case
from src.core.sale_event.sale_event_repo import ISaleEventRepo, SaleEventRepo
from src.core.voucher.voucher_repo import IVoucherRepo, VoucherRepo
from src.core.todays_top_pick.entities import FeaturableTypeEnum, TodaysTopPick
from src.core.todays_top_pick.use_case import get_todays_top_pick
from src.delivery.http.routers.common.responses import (
    SaleEventResponseObject,
    VoucherResponseObject,
)
from src.common.base_model import BaseModel, Cloner


router = APIRouter()

# TODO: add additional support for types in the future
Featurable: TypeAlias = SaleEventResponseObject | VoucherResponseObject

GetTodaysTopPicksAttributesFeaturableDataTypeEnum = StrEnum(
    "GetTodaysTopPicksAttributesFeaturableDataType",
    {member: pascal_case_to_snake_case(member.value) for member in FeaturableTypeEnum},
)


# TODO: Review and add Field defaults and documentation
class GetTodaysTopPicksAttributesFeaturableData(BaseModel):
    id: str
    type: GetTodaysTopPicksAttributesFeaturableDataTypeEnum


class GetTodaysTopPicksAttributesFeaturable(BaseModel):
    data: GetTodaysTopPicksAttributesFeaturableData


class GetTodaysTopPicksRelationships(BaseModel):
    featurable: GetTodaysTopPicksAttributesFeaturable


class GetTodaysTopPicksAttributes(Cloner[TodaysTopPick]):
    """
    Structure of attributes for API payload TodaysTopPicks.

    Currently only includes position.
    """

    _included_fields = ["position"]


class GetTodaysTopPicksData(BaseModel):
    id: str
    type: str = "todays_top_pick"
    attributes: GetTodaysTopPicksAttributes
    relationships: GetTodaysTopPicksRelationships


class GetTodaysTopPicksResponse(BaseModel):
    data: list[GetTodaysTopPicksData]
    included: list[Featurable]

    @classmethod
    def create_from_todays_top_pick_featurable(
        cls,
        todays_top_picks: list[TodaysTopPick] = [],
        featurables: list[Featurable] = [],
    ) -> "GetTodaysTopPicksResponse":
        return cls.model_validate(
            {
                "data": [
                    {
                        "id": todays_top_pick.id,
                        "attributes": todays_top_pick.model_dump(),
                        "relationships": {
                            "featurable": {
                                "data": {
                                    "id": todays_top_pick.featurable_id,
                                    "type": GetTodaysTopPicksAttributesFeaturableDataTypeEnum[
                                        todays_top_pick.featurable_type
                                    ],
                                }
                            }
                        },
                    }
                    for todays_top_pick in todays_top_picks
                ],
                "included": featurables,
            }
        )


def _group_by_featurable_type(
    top_picks: list[TodaysTopPick],
) -> dict[FeaturableTypeEnum, list[TodaysTopPick]]:
    """Given a list group TodaysTopPicks group by featureable_type."""
    res = defaultdict(list)
    for top_pick in top_picks:
        res[top_pick.featurable_type].append(top_pick)
    return res


def _get_non_none_featureable_ids(today_top_picks: list[TodaysTopPick]) -> list[str]:
    # Some ids might be None, filter and cast to str.
    return [
        str(t.featurable_id) for t in today_top_picks if t.featurable_id is not None
    ]


def _get_sale_events(
    sale_event_top_picks: list[TodaysTopPick], sale_event_repo: ISaleEventRepo
) -> list[SaleEventResponseObject]:
    ids = _get_non_none_featureable_ids(sale_event_top_picks)
    sale_events = sale_event_repo.get_by_ids(ids)

    return [
        SaleEventResponseObject.create_from_sale_event(sale_event)
        for sale_event in sale_events
    ]


def _get_vouchers(
    voucher_top_picks: list[TodaysTopPick], voucher_repo: IVoucherRepo
) -> list[VoucherResponseObject]:
    ids = _get_non_none_featureable_ids(voucher_top_picks)
    vouchers = voucher_repo.get_by_ids(ids)

    return [VoucherResponseObject.create_from_voucher(voucher) for voucher in vouchers]


@router.get("/todays_top_picks")
def get_todays_top_picks(
    sale_event_repo: Annotated[ISaleEventRepo, Depends(lambda: SaleEventRepo())],
    voucher_repo: Annotated[IVoucherRepo, Depends(lambda: VoucherRepo())],
) -> GetTodaysTopPicksResponse:
    if not (todays_top_picks := get_todays_top_pick()):
        return GetTodaysTopPicksResponse.create_from_todays_top_pick_featurable()

    featurables = []
    grouped_todays_top_picks = _group_by_featurable_type(todays_top_picks)
    for type, top_picks in grouped_todays_top_picks.items():
        if type == FeaturableTypeEnum.SALE_EVENT:
            featurables.extend(_get_sale_events(top_picks, sale_event_repo))
        elif type == FeaturableTypeEnum.VOUCHER:
            featurables.extend(_get_vouchers(top_picks, voucher_repo))
        else:
            # NOTE: If reaches here it means we have an unsupported type
            # TODO: Log error
            # Don't raise error so we can still return the supported ones
            continue

    return GetTodaysTopPicksResponse.create_from_todays_top_pick_featurable(
        todays_top_picks, featurables
    )
