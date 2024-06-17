import pytest

from src.core.suggestion.global_suggestion_elastic_search_processor import (
    GlobalSuggestionElasticSearchProcessor,
)
from src.core.suggestion.suggestion_repo import (
    GlobalSuggestionRequest,
)
from tests.helpers.test_case_helper import BaseTestCase

from tests.unit.core.suggestion.expected_response_data import *
from tests.unit.core.suggestion.mock_elastic_search_responses import *


class GenerateQueryTestCase(BaseTestCase):
    input: GlobalSuggestionRequest
    expected_output: str


@pytest.mark.parametrize(
    "test_case",
    [
        GenerateQueryTestCase(
            name="Query with 'nike'",
            input=GlobalSuggestionRequest(query="nike"),
            expected_output=(
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "preemptive_autocomplete_template", "params": {"query": "nike"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "brand_autocomplete_template", "params": {"query": "nike"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "department_autocomplete_template", "params": {"query": "nike"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "product_autocomplete_template", "params": {"query": "nike"}} \r\n'
            ),
        ),
        GenerateQueryTestCase(
            name="Query with 'iPhone'",
            input=GlobalSuggestionRequest(query="iPhone"),
            expected_output=(
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "preemptive_autocomplete_template", "params": {"query": "iPhone"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "brand_autocomplete_template", "params": {"query": "iPhone"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "department_autocomplete_template", "params": {"query": "iPhone"}} \r\n'
                '{"index": "a_deals_autocomplete"} \r\n'
                '{"id": "product_autocomplete_template", "params": {"query": "iPhone"}} \r\n'
            ),
        ),
    ],
    ids=GenerateQueryTestCase.get_name,
)
def test_generate_query(test_case: GenerateQueryTestCase):
    output_query = GlobalSuggestionElasticSearchProcessor().generate_query(
        test_case.input
    )
    assert output_query == test_case.expected_output


class GetGlobalSuggestionsTestCase(BaseTestCase):
    input: dict
    expected_output: dict


@pytest.mark.parametrize(
    "test_case",
    [
        GetGlobalSuggestionsTestCase(
            name="Get Global suggestions returns with expected structure",
            input=MockElasticSearchResponse01,
            expected_output=ExpectedResponse01,
        ),
        GetGlobalSuggestionsTestCase(
            name="When Elastic Search returns empty buckets get_global_suggestions  should returns an empty list data",
            input=MockElasticSearchResponse02,
            expected_output=ExpectedResponse02,
        ),
        GetGlobalSuggestionsTestCase(
            name="When requesting without pagecontext_key or pagecontext_value, get_global_suggestions should returns an "
            "empty list for pagecontext_suggest",
            input=MockElasticSearchResponse03,
            expected_output=ExpectedResponse03,
        ),
        GetGlobalSuggestionsTestCase(
            name="When Elastic Search returns one of it's responses with an error, we default data to empty list",
            input=MockElasticSearchResponse04,
            expected_output=ExpectedResponse04,
        ),
    ],
    ids=GetGlobalSuggestionsTestCase.get_name,
)
def test_get_global_suggestions(test_case: GetGlobalSuggestionsTestCase):
    response = GlobalSuggestionElasticSearchProcessor().parse_response(test_case.input)
    assert response.model_dump() == test_case.expected_output
