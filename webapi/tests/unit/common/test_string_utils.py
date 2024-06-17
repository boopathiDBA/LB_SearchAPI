from src.common.string_utils import pascal_case_to_snake_case, pretty_count


def test_pretty_count() -> None:
    assert pretty_count(1) == "1"
    assert pretty_count(1.111111) == "1.111111"
    assert pretty_count(999) == "999"
    assert pretty_count(500) == "500"

    assert pretty_count(1000) == "1K"
    assert pretty_count(1000.1) == "1K"
    assert pretty_count(5000) == "5K"
    assert pretty_count(1234) == "1K"
    assert pretty_count(9999) == "9K"

    assert pretty_count(10000) == "10K"
    assert pretty_count(1000.11111) == "1K"
    assert pretty_count(50000) == "50K"
    assert pretty_count(12345) == "12K"
    assert pretty_count(99999) == "99K"

    assert pretty_count(100000) == "100K"
    assert pretty_count(100000.11111) == "100K"
    assert pretty_count(500000) == "500K"
    assert pretty_count(123456) == "123K"
    assert pretty_count(999999) == "999K"

    assert pretty_count(1000000) == "1M"
    assert pretty_count(1000000.11111) == "1M"
    assert pretty_count(5000000) == "5M"
    assert pretty_count(1234567) == "1M"
    assert pretty_count(9999999) == "9M"

    assert pretty_count(10000000) == "10M"
    assert pretty_count(10000000.11111) == "10M"
    assert pretty_count(50000000) == "50M"
    assert pretty_count(12345678) == "12M"
    assert pretty_count(99999999) == "99M"

    assert pretty_count(100000000) == "100M"
    assert pretty_count(100000000.11111) == "100M"
    assert pretty_count(500000000) == "500M"
    assert pretty_count(123456789) == "123M"
    assert pretty_count(999999999) == "999M"

    assert pretty_count(1000000000) == "999M+"
    assert pretty_count(1000000000.11111) == "999M+"
    assert pretty_count(5000000000) == "999M+"
    assert pretty_count(1234567890) == "999M+"
    assert pretty_count(9999999999) == "999M+"


def test_pascal_case_to_snake_case() -> None:
    assert pascal_case_to_snake_case("Coupon") == "coupon"
    assert pascal_case_to_snake_case("SaleEvent") == "sale_event"
