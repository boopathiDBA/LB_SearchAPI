from typing import Annotated

from fastapi import Query
from pydantic import BeforeValidator

from src.core.common.repository import OrderDirectionEnum


def _maybe_set_lower(v: str) -> str:
    if isinstance(v, str):
        return v.lower()
    else:
        return v


PageNumberQueryParam = Annotated[int | None, Query(ge=1)]

PerPageQueryParam = Annotated[int | None, Query(ge=1, le=50)]

OrderByDirectionQueryParam = Annotated[
    OrderDirectionEnum | None,
    Query(
        alias="by_order[direction]",
        examples=[OrderDirectionEnum.ASC, OrderDirectionEnum.DESC],
    ),
    BeforeValidator(_maybe_set_lower),
]
