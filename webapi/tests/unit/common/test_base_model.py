import pytest
from pydantic import Field, field_validator, model_validator

from src.common.base_model import BaseModel, Cloner, MissingField


class MockModel(BaseModel):
    a: str = Field(default="default for attribute a")
    b: str
    c: str
    d: str

    # Currently there is a bug, where check_fields needs to be set to False if you would like to exclude a field
    # with a field validator
    @field_validator("a", mode="before", check_fields=False)
    @classmethod
    def _set_a(cls, a: str) -> str:
        return "overridden from field validator"

    @model_validator(mode="before")
    @classmethod
    def _set_c(cls, data: any) -> any:
        data["c"] = "overridden from model validator"
        return data


def test_cloner_metaclass_included_fields():
    class CloneIncludedModel(Cloner[MockModel]):
        _included_fields = ["a"]

    assert CloneIncludedModel.__name__ == "CloneIncludedModel"
    # Should only include field 'a' since it was configured to be included
    assert CloneIncludedModel.model_fields.keys() == {"a"}
    # Field should be identical to the original model
    for field_name in CloneIncludedModel.model_fields.keys():
        assert str(CloneIncludedModel.model_fields[field_name]) == str(
            MockModel.model_fields[field_name]
        )
    assert CloneIncludedModel.model_fields["a"].annotation == str


def test_cloner_metaclass_excluded_fields():
    class CloneExcludedModel(Cloner[MockModel]):
        _excluded_fields = ["b", "c"]

    assert CloneExcludedModel.__name__ == "CloneExcludedModel"
    assert CloneExcludedModel.model_fields.keys() == {"a", "d"}
    # Field should be identical to the original model
    for field_name in CloneExcludedModel.model_fields.keys():
        assert str(CloneExcludedModel.model_fields[field_name]) == str(
            MockModel.model_fields[field_name]
        )
    assert CloneExcludedModel.model_fields["a"].annotation == str


def test_cloner_metaclass_supports_field_validator():
    class ClonedWithField(Cloner[MockModel]):
        _included_fields = ["a"]

    clone_instance = ClonedWithField(a="to be overridden")

    # Value of a is overridden by the field validator in MockModel
    assert clone_instance.a == "overridden from field validator"


def test_cloner_supports_field_overriding():
    class ClonedOverrideField(Cloner[MockModel]):
        _included_fields = ["b"]
        # Override MockModel str field
        b: list[int]

    assert ClonedOverrideField(b=[1]).b == [1]


def test_cloner_metaclass_supports_model_validator():
    class CloneWithModelValidator(Cloner[MockModel]):
        _included_fields = ["c"]

    clone_instance = CloneWithModelValidator(c="test")

    # Value of a is overridden by the model validator in MockModel
    assert clone_instance.c == "overridden from model validator"


def test_cloner_metaclass_invalid_included_excluded_fields():
    with pytest.raises(MissingField):

        class InvalidCloneModel(Cloner[MockModel]):
            _included_fields = ["invalid_field"]

    with pytest.raises(MissingField):

        class InvalidCloneModel(Cloner[MockModel]):
            _excluded_fields = ["invalid_field"]


def test_cloner_exclude_field_with_field_validator():
    # Below should not raise an error
    class CloneWithFieldValidator(Cloner[MockModel]):
        _excluded_fields = ["a"]


def test_cloner_exclude_field_with_model_validator_that_assigns_value():
    # Below should not raise an error
    class Cloned(Cloner[MockModel]):
        _excluded_fields = ["c"]
