import json
from collections import defaultdict
from enum import StrEnum
from pathlib import Path
from typing import Protocol, TypeAlias

from jinja2 import Environment, FileSystemLoader, Template as JinjaTemplate

from src.common.base_model import BaseModel


class ElasticSearchTemplateResposeTypeEnum(StrEnum):
    """Supported response type.

    If this Enum is extended, ensure that `apply_data` method handles accordingly."""

    STR = "STR"
    DICT = "DICT"


TemplateFileName: TypeAlias = str
TemplateDirectory: TypeAlias = str
AppliedTemplate: TypeAlias = str | dict


class IElasticSearchTemplate(Protocol):
    def apply_data(
        self,
        args: BaseModel,
        response_type: ElasticSearchTemplateResposeTypeEnum = ElasticSearchTemplateResposeTypeEnum.DICT,
    ) -> AppliedTemplate:
        """
        Apply args values to elastic search template
        """
        pass


class ElasticSearchTemplate(IElasticSearchTemplate):
    # Class variable that holds loaded environments. This is used to reduce multiple loading of the same directory
    _jinga_environments: dict[TemplateFileName, Environment] = defaultdict()

    def __init__(
        self,
        template_file_name: TemplateFileName,
        template_directory: TemplateDirectory = f"{str(Path(__file__).resolve().parent.parent.parent)}/adapters"
        f"/elastic_search/templates",
    ):
        self._template_directory = template_directory
        self._template_file_name = template_file_name

        self._jinja_environment = ElasticSearchTemplate._get_jinja_environment(
            self._template_directory
        )
        self._jinja_template = self._load_jinja_template()

    @classmethod
    def _get_jinja_environment(
        cls, template_directory: TemplateDirectory
    ) -> Environment:
        """Return Environment if one already exist for directory. Otherwise, load a new one and store for later use."""
        if template_directory in cls._jinga_environments:
            return cls._jinga_environments[template_directory]

        environment = cls._load_jinja_environment(template_directory)
        cls._jinga_environments[template_directory] = environment
        return environment

    @classmethod
    def _load_jinja_environment(
        cls, template_directory: TemplateDirectory
    ) -> Environment:
        environment = Environment(loader=FileSystemLoader(template_directory))
        environment.filters["jsonify"] = json.dumps
        return environment

    def _load_jinja_template(self) -> JinjaTemplate:
        return self._jinja_environment.get_template(self._template_file_name)

    def apply_data(
        self,
        args: BaseModel,
        response_type: ElasticSearchTemplateResposeTypeEnum = ElasticSearchTemplateResposeTypeEnum.DICT,
    ) -> AppliedTemplate:
        """
        Apply arguments to template.

        Parameters:
            args (BaseModel): data to be appled to template
            response_type (ElasticSearchTemplateResposeTypeEnum): Type of response to return.
        """
        res_str = self._jinja_template.render(args=args)

        if response_type == ElasticSearchTemplateResposeTypeEnum.STR:
            return res_str
        elif response_type == ElasticSearchTemplateResposeTypeEnum.DICT:
            return json.loads(res_str)
        else:
            raise ValueError(f"Unsupported response_type: {response_type}")
