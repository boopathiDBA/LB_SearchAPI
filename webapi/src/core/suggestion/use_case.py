from src.core.suggestion.entities import ElasticSearchSuggestion
from src.core.suggestion.suggestion_repo import (
    GlobalSuggestionRequest,
    SuggestionRepo,
    ISuggestionRepo,
)


def get_global_suggestions(
    request: GlobalSuggestionRequest,
    suggestion_repo: ISuggestionRepo = SuggestionRepo(),
) -> ElasticSearchSuggestion:
    return suggestion_repo.get_global_suggestions(request)
