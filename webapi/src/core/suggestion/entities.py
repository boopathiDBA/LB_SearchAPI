from pydantic import Field, create_model

from src.common.base_model import BaseModel
from src.core.common.base_entity import BaseEntity


def _create_main_suggestion(name: str) -> type[BaseModel]:
    """
    Dynamically creates a pydandic model based on the name.

    An example if name is passed in as `brand` the resulting model is as follows:

    {
        data: {
            ...
            _id: str
            _source: { brand_name: str, brand_slug: str, brand_logo: str }
        }
    }

    :param name: Name of the model to create
    :return: Pydantic model
    """
    source_fields = {
        f"{name}_name": (str, Field()),
        f"{name}_slug": (str | None, Field(default=None)),
        f"{name}_logo": (str | None, Field(default=None)),
    }
    source_model = create_model(
        f"{name.capitalize()}MainSuggestionDataSource", **source_fields
    )

    # Alias is used since pydantic interprets `_` prefix as private (hidden) fields
    main_data_fields = {
        "index": (str, Field(alias="_index")),
        "id": (str, Field(alias="_id")),
        "score": (float, Field(alias="_score")),
        "source": (source_model, Field(alias="_source")),
    }
    main_data_model = create_model(
        f"{name.capitalize()}MainSuggestionData", **main_data_fields
    )

    main_suggestion_fields = {"data": (list[main_data_model], [])}
    main_suggestion_model = create_model(
        f"{name.capitalize()}MainSuggestion", **main_suggestion_fields
    )

    return main_suggestion_model


class KeyDocCount(BaseModel):
    key: str
    doc_count: int


class KeyDocCountData(BaseModel):
    data: list[KeyDocCount] = []


StoreMainSuggestion = _create_main_suggestion(name="store")
BrandMainSuggestion = _create_main_suggestion(name="brand")
CategoryMainSuggestion = _create_main_suggestion(name="category")
DepartmentMainSuggestion = _create_main_suggestion(name="department")
SubcategoryMainSuggestion = _create_main_suggestion(name="subcategory")


class ElasticSearchSuggestion(BaseEntity):
    preemptive_category_suggestion: KeyDocCountData
    preemptive_subcategory_suggestion: KeyDocCountData
    store_main: StoreMainSuggestion
    brand_main: BrandMainSuggestion
    category_main: CategoryMainSuggestion
    department_main: DepartmentMainSuggestion
    subcategory_main: SubcategoryMainSuggestion
    pagecontext_suggest: KeyDocCountData
    product_suggestion: KeyDocCountData
