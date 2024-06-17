from fastapi import APIRouter
from fastapi import status

from src.common.base_model import BaseModel
from src.core.suggestion.entities import ElasticSearchSuggestion
from src.core.suggestion.suggestion_repo import GlobalSuggestionRequest
from src.core.suggestion.use_case import (
    get_global_suggestions as get_global_suggestions_use_case,
)

router = APIRouter()


class GetGlobalSuggestionResponse(BaseModel):
    suggestions: ElasticSearchSuggestion


@router.post("/global_suggessions", status_code=status.HTTP_201_CREATED)
def get_global_suggestion(body: GlobalSuggestionRequest) -> GetGlobalSuggestionResponse:
    return GetGlobalSuggestionResponse(
        suggestions=get_global_suggestions_use_case(body)
    )
