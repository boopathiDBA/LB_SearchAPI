from pydantic import Field

from src.common.base_model import BaseModel


class BaseTestCase(BaseModel):
    # Set __test__ to False to prevent pytest collection warning
    __test__ = False

    name: str = Field(
        description="Name of the test case",
        examples=["Test get global suggestions with query"],
    )

    def get_name(self):
        """Method that is used by pytest to return name of the test instead of pytest's
        default behaviour which is a randomly generated number."""
        return self.name
