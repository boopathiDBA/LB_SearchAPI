from datetime import datetime

from pydantic import model_validator

from src.common.base_model import BaseModel
from src.core.common.field_types import UtcDatetime


class ExperimentVariant(BaseModel):
    # Allow for None as UAT may contain dirty data.
    id: int | None
    name: str | None
    weight: str | None
    content: str | None
    property: int | None


class Experiment(BaseModel):
    id: int
    name: str
    state: str
    active: bool
    version: int
    variants: list[ExperimentVariant]
    updated_at: UtcDatetime

    @model_validator(mode="before")
    @classmethod
    def _maybe_set_version(cls, data: any) -> any:
        """Set version before validatation.
        Version is derived from updated_at as unix time as an int"""
        if isinstance(data.get("updated_at"), datetime):
            data["version"] = int(data["updated_at"].timestamp())

        return data
