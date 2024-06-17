from enum import StrEnum


class UnitEnum(StrEnum):
    THOUSAND = "K"
    MILLION = "M"


def _crop(n: float, precision: int) -> str:
    significant_digits = len(str(int(n)))
    if precision > significant_digits:
        return str(n)[: precision + 1]
    else:
        return str(int(n))


def _number_to_human(n: float, precision: int) -> str:
    if n < 1_000:
        return str(n)
    elif n < 1_000_000:
        return _crop(n / 1_000, precision) + UnitEnum.THOUSAND
    else:
        return _crop(n / 1_000_000, precision) + UnitEnum.MILLION


def pretty_count(count: int | float) -> str:
    if 0 <= count <= 999:
        return str(count)
    elif 1_000 <= count <= 9_999 or 1_000_000 <= count <= 9_999_999:
        return _number_to_human(count, 1).replace(" ", "")
    elif 10_000 <= count <= 99_999 or 10_000_000 <= count <= 99_999_999:
        return _number_to_human(count, 2).replace(" ", "")
    elif 100_000 <= count <= 999_999 or 100_000_000 <= count <= 999_999_999:
        return _number_to_human(count, 3).replace(" ", "")
    else:
        return "999M+"


def pascal_case_to_snake_case(s: str) -> str:
    """Return snake_case of PascalCase string.

    e.g.
        "SaleEvent" -> "sale_event"
        "Coupon" -> "coupon"
    """
    return "".join(["_" + c.lower() if c.isupper() else c for c in s]).lstrip("_")


def number_to_currency(num):
    if num.is_integer():
        return "${:,.0f}".format(num)
    else:
        return "${:,.2f}".format(num)
