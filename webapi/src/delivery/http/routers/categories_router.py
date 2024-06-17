from fastapi import status, APIRouter, Depends
from pydantic import Field

from src.common.base_model import BaseModel
from src.core.category.category_repo import CategoryRequest
from src.core.category.entities import Category
from src.core.category.usecase import get_categories_by_filters
from src.delivery.http.http_exceptions import NotFoundHttpException

router = APIRouter(prefix="/categories")


class CategoryRelationshipData(BaseModel):
    id: str
    type: str


class CategoryRelationship(BaseModel):
    data: CategoryRelationshipData


class CategoryResponseObject(BaseModel):
    """
    Structure of the categories list response
    """

    id: str
    type: str = "category"
    attributes: Category
    relationships: CategoryRelationship


class CategoryListMeta(BaseModel):
    order: list[int | None] = []


class CategoryListResponse(BaseModel):
    data: list[CategoryResponseObject] = []
    meta: CategoryListMeta = Field(default_factory=CategoryListMeta)


@router.get("", status_code=status.HTTP_200_OK)
def list_categories(body: CategoryRequest = Depends()) -> CategoryListResponse:
    categories = get_categories_by_filters(body)

    return CategoryListResponse.model_validate(
        {
            "data": [
                {
                    "id": category.id,
                    "attributes": category,
                    "relationships": {
                        "data": {"id": body.by_department, "type": "department"}
                    },
                }
                for category in categories
                if category.active == body.by_active
            ],
            "meta": {
                "order": [
                    int(category.id) if category.active else None
                    for category in categories
                ],
            },
        }
    )
