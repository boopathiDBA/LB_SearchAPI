from pydantic import Field, model_validator

from src.core.common.base_entity import BaseEntity


class Department(BaseEntity):
    """
    Structure of the DB table
    """

    id: str = Field(description="Department identifier", examples=["94"])
    name: str = Field(description="Department name", examples=["Fashion"])
    slug: str = Field(description="Department slug", examples=["fashion"])
    position: int = Field(description="position for department ", examples=["1"])
    active: bool = Field(description="Department active status")
    popular: bool = Field(description="Department popular status")
    color: str = Field(description="Department color code", examples=["f3f4f3"])
    intro: str = Field(default="", description="intro value")
    icon: str | None = Field(
        description="Department icon image", examples=["fashion.png"]
    )
    desktop_banner: str | None = Field(
        description="Department desktop banner image", examples=["fashion.png"]
    )
    mobile_banner: str | None = Field(
        description="Department icon image", examples=["fashion.png"]
    )

    # category_ids field is derived from related categories table
    category_ids: list[str] = Field(
        default=[], description="list of ids of related categories"
    )

    @model_validator(mode="before")
    @classmethod
    def _remove_null_category_ids(cls, data: any) -> any:
        """Remove all null/None values from category_ids list

        This currently is required as the SQL query may return departments with category_ids as
        a list of null. e.g. [None].

        This scenario happens when there exist a department which has no
        related categories.
        """

        if isinstance(data, dict) and (
            (category_ids := data.get("category_ids", None)) is not None
        ):
            data["category_ids"] = [
                category_id for category_id in category_ids if category_id is not None
            ]

        return data
