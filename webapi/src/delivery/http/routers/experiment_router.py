from collections import defaultdict, Counter
from enum import StrEnum

from fastapi import APIRouter
from pydantic import Field
from pydantic import create_model

from src.common.base_model import BaseModel, Cloner
from src.core.experiment.entities import Experiment
from src.core.experiment.usecase import get_experiments

router = APIRouter(prefix="/experiments")


class ExperimentStateEnum(StrEnum):
    CREATED = "created"
    CHANGED = "changed"
    DELETED = "deleted"

    @classmethod
    def values(cls) -> list[str]:
        return [enum_value.value for enum_value in cls]


class ExperimentResponse(Cloner[Experiment]):
    _excluded_fields = ["updated_at"]


def _get_experiment_data_response_model() -> type[BaseModel]:
    """Dynamically creates a pydandic model.

    Since there is a key for each Experiment state, this function creates the model based on the values in
    the enum ExperimentStateEnum.

    e.g. A object of this model is as follows:
    {
        created: list[ExperimentResponse] = Field(...),
        changed: list[ExperimentResponse] = Field(...),
        deleted: list[ExperimentResponse] = Field(...)
        ...<any additional state>: ExperimentResponse = Field(...)
    }
    """
    fields = {
        state: (
            list[ExperimentResponse],
            Field(default=None, description=f"Experiments with the {state} state"),
        )
        for state in ExperimentStateEnum.values()
    }

    return create_model("GetExperimentsDataResponse", **fields)


GetExperimentsDataResponse = _get_experiment_data_response_model()


def _get_experiments_response_model() -> type[BaseModel]:
    """Dynamically creates a pydandic model.

    Since there is a key for each Experiment state, this function creates the model based on the values in
    the enum ExperimentStateEnum.

    e.g. A object of this model is as follows:
    {
        data: GetExperimentsDataResponse
        created: int = Field(...),
        changed: int = Field(...),
        deleted: int = Field(...),
        ...<any additional states>: int = Field(...),
    }
    """
    fields = {
        state: (
            int,
            Field(
                default=0, description=f"The number of experiments in a {state} state"
            ),
        )
        for state in ExperimentStateEnum.values()
    }
    fields["data"] = (GetExperimentsDataResponse, Field(description="Experiments data"))

    return create_model("GetExperimentsResponse", **fields)


class GetExperimentsResponse(_get_experiments_response_model()):
    @classmethod
    def create_from_experiments(
        cls, experiments: list[Experiment]
    ) -> "GetExperimentsResponse":
        """Factory method to create a GetExperimentsDataResponse from a list of experiments."""
        experiments_grouped_by_state = cls._dict_and_group_experiments_by_state(
            experiments
        )
        state_to_count_mapping = Counter(
            [experiment.state for experiment in experiments]
        )

        return GetExperimentsResponse.model_validate(
            {
                **state_to_count_mapping,
                "data": experiments_grouped_by_state,
            }
        )

    @classmethod
    def _dict_and_group_experiments_by_state(
        cls,
        experiments: list[Experiment],
    ) -> dict[str, dict]:
        """Group experiments by state returning experiment dictionaries.
        returns a dictionary with the different states as the key and a list of experiments as the value.
        e.g. { "created": [experiment1, experiment2], "changed": [experiment3]... }
        """
        grouping = defaultdict(list)
        for experiment in experiments:
            grouping[experiment.state].append(dict(experiment))
        return grouping


@router.get("")
def list_experiments() -> GetExperimentsResponse:
    experiments = get_experiments()

    return GetExperimentsResponse.create_from_experiments(experiments)
