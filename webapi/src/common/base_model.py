from __future__ import annotations

import copy
import typing
from unittest import mock

from pydantic import (
    BaseModel as PydanticBaseModel,
    model_validator,
    ConfigDict,
)
from pydantic._internal._fields import collect_model_fields
from pydantic._internal._generics import get_model_typevars_map
from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core import PydanticUndefined


class BaseModel(PydanticBaseModel):
    """
    BaseModel that Inherited instead of Pydantic's. This ensures all models contain the same functionality
    """

    model_config = ConfigDict(coerce_numbers_to_str=True)

    @model_validator(mode="before")
    @classmethod
    def _maybe_set_default_for_none_value(cls, data: any) -> any:
        """
        If None is passed in as a value and default or default_factory is configured, set to default.

        The usual behaviour of Pydantic models, when a field is configured with a default. eg. field_name: str = ""
        and a instance is created MyClass(field_name=None) this raises an validation error.

        This model validator bypasses this error by setting the configured default value.
        """
        if type(data) is not dict:
            return data

        fields_with_default = {
            field_name: field.default
            for field_name, field in cls.model_fields.items()
            if type(field.default).__name__ != "PydanticUndefinedType"
        }

        fields_with_default_factory = {
            field_name: field.default_factory
            for field_name, field in cls.model_fields.items()
            if field.default_factory is not None
        }

        for field_name, value in data.items():
            if value is None:
                if field_name in fields_with_default.keys():
                    data[field_name] = fields_with_default[field_name]
                elif field_name in fields_with_default_factory.keys():
                    data[field_name] = fields_with_default_factory[field_name]()

        return data


class MissingField(Exception):
    pass


ClonedModelType = typing.TypeVar("ClonedModelType")


class ClonerMeta(type):
    """See Cloner documentation below"""

    def __new__(mcs, name, bases, namespace, **kwargs):
        if name == "Cloner" and namespace["__module__"] == ClonerMeta.__module__:
            return super().__new__(mcs, name, bases, namespace, **kwargs)
        if "__annotations__" not in namespace:
            namespace["__annotations__"] = {}

        # Assumes there's exactly one base for the wrapper subclass...
        # This could be modified for multiple inheritence, if needed...
        original_model: type[PydanticBaseModel] = typing.get_args(
            namespace["__orig_bases__"][0]
        )[0]

        namespace["__annotations__"]["_included_fields"] = typing.ClassVar[list[str]]
        namespace["__annotations__"]["_excluded_fields"] = typing.ClassVar[list[str]]

        included_fields = namespace.get("_included_fields", [])
        excluded_fields = namespace.get("_excluded_fields", [])
        if included_fields and excluded_fields:
            raise ValueError(
                "Must only define included_fields OR excluded_fields, not both."
            )

        # Note. Previously `copy.deepcopy` was used here, but this caused issues.
        kls = ModelMetaclass("Cloner", (PydanticBaseModel,), copy.copy(namespace))

        def new_set_model_fields(
            cls, real_bases, config_wrapper, types_namespace
        ) -> None:
            typevars_map = get_model_typevars_map(cls)
            fields, class_vars = collect_model_fields(
                cls,
                real_bases + (kls,),
                config_wrapper,
                types_namespace,
                typevars_map=typevars_map,
            )

            if invalid_included_fields := set(included_fields) - set(fields.keys()):
                raise MissingField(
                    f"Field names to include: {' ,'.join(invalid_included_fields)},  does not exist in model: {original_model}"
                )

            if invalid_excluded_fields := set(excluded_fields) - set(fields.keys()):
                raise MissingField(
                    f"Field names to excluded: {' ,'.join(invalid_excluded_fields)},  does not exist in model: {original_model}"
                )

            new_fields = {}
            for field_name, info in fields.items():
                if (
                    included_fields
                    and field_name in included_fields
                    and field_name not in namespace
                ):
                    new_fields[field_name] = info
                elif (
                    excluded_fields
                    and field_name not in excluded_fields
                    and field_name not in namespace
                ):
                    new_fields[field_name] = info
                elif (
                    not included_fields
                    and not excluded_fields
                    and field_name not in namespace
                ):
                    new_fields[field_name] = info
                if field_name in namespace:
                    new_fields[field_name] = info
            cls.model_fields = new_fields
            cls.__class_vars__.update(class_vars)
            for k in class_vars:
                value = cls.__private_attributes__.pop(k, None)
                if value is not None and value.default is not PydanticUndefined:
                    setattr(cls, k, value.default)

        with mock.patch(
            "pydantic._internal._model_construction.set_model_fields",
            new=new_set_model_fields,
        ):
            klass = ModelMetaclass.__new__(
                ModelMetaclass, name, (original_model,), namespace, **kwargs
            )
        return klass


class Cloner(typing.Generic[ClonedModelType], metaclass=ClonerMeta):
    """Cloner metaclass that clones another BaseModel definition (fields, validators).

    This currently supports two class variables which determine which fields will be included/excluded.
    See unit test for example usage.

    This code was taken and modified from https://github.com/pydantic/pydantic/discussions/2686

    """

    pass
