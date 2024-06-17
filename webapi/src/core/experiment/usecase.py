from src.core.experiment.entities import Experiment
from src.core.experiment.experiment_repo import IExperimentRepo, ExperimentRepo


def get_experiments(
    experiment_repo: IExperimentRepo = ExperimentRepo(),
) -> list[Experiment]:
    return experiment_repo.get_experiments()
