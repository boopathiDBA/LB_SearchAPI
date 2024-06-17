import json

import pytest

from src.adapters.elastic_search.elastic_search_processor import ElasticSearchQuery
from src.core.common.user_affinity.user_affinity_request import UserAffinityRequest
from src.core.sale_event.entities import ElasticSearchUserAffinitySaleEvent
from src.core.sale_event.user_affinity_sale_events_elastic_search_processor import (
    UserAffinitySaleEventsElasticSearchProcessor,
)
from tests.helpers.test_case_helper import BaseTestCase
from tests.unit.core.sale_event.user_affinity_sale_events_elastic_processor.expected_outputs import *
from tests.unit.core.sale_event.user_affinity_sale_events_elastic_processor.mock_inputs import *

"""These test only test the UserAffinitySaleEventsProcessor as it has common code to UserAffinityVouchersProcessor"""


class GenerateQueryTestCase(BaseTestCase):
    input: UserAffinityRequest
    expected_output: ElasticSearchQuery


@pytest.mark.parametrize(
    "test_case",
    [
        GenerateQueryTestCase(
            name="Expect Affinities are injected into query",
            input=UserAffinityRequest.model_validate(mock_query_input_01),
            expected_output=expected_query_output_01,
        ),
        GenerateQueryTestCase(
            name="Expect filters are injected into query",
            input=UserAffinityRequest.model_validate(mock_query_input_02),
            expected_output=expected_query_output_02,
        ),
        GenerateQueryTestCase(
            name="When gender request is male expect query term to be added",
            input=UserAffinityRequest.model_validate(mock_query_input_03),
            expected_output=expected_query_output_03,
        ),
        GenerateQueryTestCase(
            name="When gender request is female expect query term to be added",
            input=UserAffinityRequest.model_validate(mock_query_input_04),
            expected_output=expected_query_output_04,
        ),
    ],
    ids=GenerateQueryTestCase.get_name,
)
def test_generate_query(test_case: GenerateQueryTestCase):
    builder = UserAffinitySaleEventsElasticSearchProcessor()
    builder.generate_query(test_case.input)

    assert builder.generate_query(test_case.input) == test_case.expected_output


class ParseResponseTestCase(BaseTestCase):
    # pass
    input: dict
    expected_output: list[dict]


@pytest.mark.parametrize(
    "test_case",
    [
        ParseResponseTestCase(
            name="Test response defaults to empty list when Elastic Search returns an error",
            input=mock_search_elastic_response_01,
            expected_output=expected_parse_response_output_01,
        ),
        ParseResponseTestCase(
            name="Test mutiple items from the same store are filtered out",
            input=mock_search_elastic_response_02,
            expected_output=expected_parse_response_output_02,
        ),
        ParseResponseTestCase(
            name="Test mutiple items from the same category are filtered out",
            input=mock_search_elastic_response_03,
            expected_output=expected_parse_response_output_03,
        ),
    ],
    ids=ParseResponseTestCase.get_name,
)
def test_parse_response(test_case: ParseResponseTestCase):
    builder = UserAffinitySaleEventsElasticSearchProcessor()
    response = builder.parse_response(test_case.input)

    assert [
        json.loads(
            ElasticSearchUserAffinitySaleEvent.model_validate(item).model_dump_json()
        )
        for item in response
    ] == test_case.expected_output
