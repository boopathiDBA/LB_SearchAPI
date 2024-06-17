from enum import StrEnum, auto

from pydantic import Field, AfterValidator
from typing_extensions import Annotated

from src.common.base_model import BaseModel


class OrderDirectionEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"


class Page(BaseModel):
    page_number: int = Field(
        default=1,
        description="Page number for the pagination request",
        examples=[1, 2, 3],
    )
    per_page: int = Field(
        default=10,
        description="Page size for the pagination request",
        examples=[10, 50],
    )


TOP_LIST_DEFAULT_PAGE = Page(page_number=1, per_page=50)


class Order(BaseModel):
    column: str = Field(
        description="Column name to order/sort on",
        examples=["name", "deals_count"],
    )
    direction: OrderDirectionEnum = Field(
        description="Order/sort direction",
        examples=["ASC", "DESC"],
    )


def check_no_whitespace(v: str):
    if v != v.strip():
        raise ValueError("Cannot contain leading or trailing whitespaces")
    return v


"""
Unique identifier like an int id or slug like 'electronics', 'jb-hifi'
for entities like 'Deal', 'Brand', 'Store' etc.
"""
FriendlyId = Annotated[str, AfterValidator(check_no_whitespace)]
