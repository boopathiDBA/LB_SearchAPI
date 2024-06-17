from pydantic import Field

from src.core.common.base_entity import BaseEntity


class Category(BaseEntity):
    """
    Structure of the DB table
    """

    id: str = Field(description="Category identifier")
    name: str = Field(description="Category name", examples=["Building Toys"])
    slug: str = Field(description="Category slug", examples=["building-toys"])
    department_id: str = Field(description="Department id of this Category")
    position: int | None = Field(default=None, description="Position for Category")
    active: bool = Field(default=False, description="Active status for Category")
    popular: bool = Field(default=False, description="Popularity status for Category")
    carousel_position: int | None = Field(
        default=None, description="Carousel Position of Category"
    )
    navbar_spacer: bool = Field(
        default=False, description="navbar_spacer value for Category"
    )
