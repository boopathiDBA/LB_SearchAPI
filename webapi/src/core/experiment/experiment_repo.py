from typing import Protocol

from psycopg2.extras import DictCursor

from src.adapters.rds_client import IRdsClient, get_initialised_rds_client
from src.core.experiment.entities import ExperimentVariant
from src.delivery.http.routers.experiment_router import Experiment


class IExperimentRepo(Protocol):
    def get_experiments(self) -> list[Experiment]:
        pass


class ExperimentRepo(IExperimentRepo):
    def __init__(
        self,
        rds_client: IRdsClient | None = get_initialised_rds_client(),
    ):
        self._rds_client = rds_client

    def _get_experiments_query_json_object_arg(self) -> str:
        """Return a string which can be used as an argument to json_build_object

        The expected format of the json_build_object function is:
            json_build_object('key', value,...)

        For reference: https://www.postgresql.org/docs/current/functions-aggregate.html
        """
        # Property field is the id of the last experiment variant change
        field_to_column_map = {
            "property": "evc.id",
        }

        experiment_variant_colum_names = [
            field_name
            for field_name in ExperimentVariant.model_fields.keys()
            if field_name not in field_to_column_map.keys()
        ]

        # Format of expected json_object_arg: 'key', value, ...
        json_object_arg = ", ".join(
            f"'{name}', ev.{name}" for name in experiment_variant_colum_names
        )

        for field_name, column_name in field_to_column_map.items():
            json_object_arg += f", '{field_name}', {column_name}"

        return json_object_arg

    def _get_experiments_query(self) -> str:
        return f"""
            SELECT e.*, 
                json_agg(json_build_object({self._get_experiments_query_json_object_arg()})) AS variants
            FROM experiments e
            LEFT JOIN experiment_variants ev ON e.id = ev.experiment_id
            LEFT JOIN (
                SELECT MAX(id) AS id, experiment_variant_id
                FROM experiment_variant_changes
                GROUP BY experiment_variant_id
            ) evc ON ev.id = evc.experiment_variant_id
            GROUP BY e.id;
        """

    def get_experiments(self) -> list[Experiment]:
        results = self._rds_client.execute_fetch_all_query(
            self._get_experiments_query(),
            [],
            DictCursor,
        )

        return [Experiment.model_validate(dict(result)) for result in results]
