from abc import abstractmethod, ABCMeta
from typing import TypeAlias, Protocol, TypeVar

from src.adapters.elastic_search.elastic_search_client import (
    ElasticSearchResult,
    IElasticSearchClient,
)
from src.adapters.elastic_search.queries.helper import ElasticSearchIndexEnum
from src.common.base_model import BaseModel

ElasticSearchQuery: TypeAlias = dict | str

TGenerateQueryArgs = TypeVar("TGenerateQueryArgs", bound=BaseModel)
TParsedResponse = TypeVar("TParsedResponse")


class IElasticSearchProcessor(Protocol[TGenerateQueryArgs, TParsedResponse]):
    """
    Interface for Elastic Search Processors.

    This interface is designed to encapsulate elastic search query generate as well as response parsing.

    This uses the template pattern. With .execute() method as the template method.

    The interface supports generics to allow for each concrete implementation may require different argument typing.
    To use generic types, the concrete implementation should inherit from this interface and provide the generic types.
    e.g. class MyProcessor(IElasticSearchProcessor[MyArgsType, MyResponseType]):

    """

    def generate_query(self, args: TGenerateQueryArgs) -> ElasticSearchQuery:
        """Given args generate a Elastic Search query"""
        pass

    def parse_response(self, response: ElasticSearchResult) -> TParsedResponse:
        """Given a Elastic Search response, parse it to the expected response type"""
        pass

    def get_index(self) -> ElasticSearchIndexEnum:
        """Return the index for the Elastic Search query"""
        pass

    def execute(
        self, client: IElasticSearchClient, args: TGenerateQueryArgs
    ) -> TParsedResponse:
        """Execute the processor. This is the template method of the template pattern"""
        pass


class ElasticSearchProcessorBase(
    Protocol[TGenerateQueryArgs, TParsedResponse], metaclass=ABCMeta
):
    @abstractmethod
    def generate_query(self, args: TGenerateQueryArgs) -> ElasticSearchQuery:
        raise NotImplementedError()

    @abstractmethod
    def parse_response(self, response: ElasticSearchResult) -> TParsedResponse:
        raise NotImplementedError()

    @abstractmethod
    def get_index(self) -> ElasticSearchIndexEnum:
        raise NotImplementedError()

    def execute(
        self, client: IElasticSearchClient, args: TGenerateQueryArgs
    ) -> TParsedResponse:
        query = self.generate_query(args)
        response = client.query_index(self.get_index(), query)
        parsed_response = self.parse_response(response)

        return parsed_response
