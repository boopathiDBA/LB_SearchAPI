from datetime import datetime

from src.core.common.field_types import UtcDatetime
from src.core.common.base_entity import BaseEntity


class MockEntity(BaseEntity):
    created_at: UtcDatetime


mock_utc_time = datetime(2023, 1, 28, 16, 0, 0)
mock_entity = MockEntity(created_at=mock_utc_time)


def test_utc_datetime_is_serialized_to_expected_timezone() -> None:
    # Assert when dumping to dict format
    entity_dict = mock_entity.model_dump()
    assert str(entity_dict["created_at"]) == "2023-01-29 03:00:00+11:00"

    # Assert when dumping to json format
    assert mock_entity.model_dump(mode="json") == {
        "created_at": "2023-01-29T03:00:00+11:00"
    }


def test_utc_datetime_is_serialized_only_once_if_nested_model_construction() -> None:
    """
    Throughout out code we may dump a model and use it to construct another model.

    If we do this we should expect any datetimes fields to be serialized to local timezone only once.
    """

    class MockEntity2(BaseEntity):
        foo: str = ""
        created_at: UtcDatetime

    # Get first dump of entity which should be serialized to local timezone
    mock_entity_dict = mock_entity.model_dump()
    first_dump_datetime = str(mock_entity_dict["created_at"])

    # Construct instance model using the dumped dict
    mock_entity_2 = MockEntity2.model_validate(mock_entity_dict)
    mock_entity_2_dict = mock_entity_2.model_dump()

    # Assert the second datetime field is the same as the first datetime field
    assert str(mock_entity_2_dict["created_at"]) == first_dump_datetime
