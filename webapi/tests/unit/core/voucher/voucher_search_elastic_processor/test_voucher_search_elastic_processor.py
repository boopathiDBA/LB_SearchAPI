import pytest

from src.core.common.elastic_search.search_elastic_processor_base import (
    ElasticSearchRequest,
)
from src.core.voucher.voucher_search_elastic_processor import (
    VoucherSearchElasticProcessor,
)
from tests.helpers.test_case_helper import BaseTestCase
from tests.unit.core.voucher.voucher_search_elastic_processor.expected_template import *
from tests.unit.core.voucher.voucher_search_elastic_processor.mock_request import *


class TestCase(BaseTestCase):
    input: ElasticSearchRequest
    expected: dict


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            name="Test when no field (i,e store_name, brand_name, etc) value provided",
            input=MockElasticSearchVouchersRequest1,
            expected=ExpectedTemplate1,
        ),
        TestCase(
            name="Test pagination",
            input=MockElasticSearchVouchersRequest2,
            expected=ExpectedTemplate2,
        ),
        TestCase(
            name="Test when brand name present",
            input=MockElasticSearchVouchersRequest3,
            expected=ExpectedTemplate3,
        ),
        TestCase(
            name="Test when category name present",
            input=MockElasticSearchVouchersRequest4,
            expected=ExpectedTemplate4,
        ),
        TestCase(
            name="Test when department name present",
            input=MockElasticSearchVouchersRequest5,
            expected=ExpectedTemplate5,
        ),
        TestCase(
            name="Test when subcategory name present",
            input=MockElasticSearchVouchersRequest6,
            expected=ExpectedTemplate6,
        ),
    ],
    ids=TestCase.get_name,
)
def test_generate_query(test_case: TestCase):
    processor = VoucherSearchElasticProcessor()
    query = processor.generate_query(test_case.input)
    assert query["params"] == test_case.expected
