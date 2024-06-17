from fastapi import status, APIRouter, Depends
from pydantic import Field, HttpUrl

from src.common.base_model import BaseModel, Cloner
from src.core.department.department_repo import (
    DepartmentRequest,
)
from src.core.department.entities import Department
from src.core.department.usecase import get_departments_by_filters
from src.delivery.http.router_helper import IMAGE_BASE_URL

router = APIRouter(prefix="/departments")

DEPARTMENT_IMAGE_URL = f"{IMAGE_BASE_URL}/department"


class DepartmentListMeta(BaseModel):
    order: list[int]


class DepartmentRelationshipCategoryData(BaseModel):
    id: str = Field(description="Category identifier")
    type: str = "category"


class DepartmentRelationshipCategoryList(BaseModel):
    data: list[DepartmentRelationshipCategoryData]


class DepartmentRelationship(BaseModel):
    categories: DepartmentRelationshipCategoryList

    @classmethod
    def create_from_department(cls, department: Department) -> "DepartmentRelationship":
        return cls.model_validate(
            {
                "categories": {
                    "data": [
                        {"id": category_id, "type": "category"}
                        for category_id in department.category_ids
                    ]
                }
            }
        )


class DepartmentLinkUrl(BaseModel):
    url: HttpUrl | None = Field(default=None, description="Department Icon URL")


class DepartmentLinkIcon(BaseModel):
    url: HttpUrl | None = Field(default=None, description="Department upload URL")
    tiny: DepartmentLinkUrl
    medium: DepartmentLinkUrl


class DepartmentLinkObject(BaseModel):
    icon: DepartmentLinkIcon
    desktop_banner: DepartmentLinkUrl
    mobile_banner: DepartmentLinkUrl

    @classmethod
    def create_from_department(cls, department: Department) -> "DepartmentLinkObject":
        department_id = department.id

        return cls.model_validate(
            {
                "icon": DepartmentLinkIcon.model_validate(
                    {
                        "url": f"{DEPARTMENT_IMAGE_URL}/icon/{department_id}/{department.icon}",
                        "tiny": {
                            "url": f"{DEPARTMENT_IMAGE_URL}/icon/{department_id}/tiny_{department.icon}"
                        },
                        "medium": {
                            "url": f"{DEPARTMENT_IMAGE_URL}/icon/{department_id}/medium_{department.icon}"
                        },
                    }
                ),
                "desktop_banner": {
                    "url": f"{DEPARTMENT_IMAGE_URL}/desktop_banner/{department_id}/{department.desktop_banner}"
                },
                "mobile_banner": {
                    "url": f"{DEPARTMENT_IMAGE_URL}/mobile_banner/{department_id}/{department.mobile_banner}"
                },
            }
        )


class DepartmentAttributes(Cloner[Department]):
    """Duplicate structure of Department but with excluded fields"""

    _excluded_fields = ["icon", "desktop_banner", "mobile_banner", "category_ids"]


class DepartmentData(BaseModel):
    id: str
    type: str = "department"
    attributes: DepartmentAttributes
    relationships: DepartmentRelationship
    links: DepartmentLinkObject

    @classmethod
    def create_from_department(cls, department: Department) -> "DepartmentData":
        return cls.model_validate(
            {
                "id": department.id,
                "attributes": DepartmentAttributes.model_validate(dict(department)),
                "relationships": DepartmentRelationship.create_from_department(
                    department
                ),
                "links": DepartmentLinkObject.create_from_department(department),
            }
        )


class DepartmentListResponse(BaseModel):
    data: list[DepartmentData]
    meta: DepartmentListMeta

    @classmethod
    def create_from_departments(
        cls, departments: list[Department]
    ) -> "DepartmentListResponse":
        return cls.model_validate(
            {
                "data": [
                    DepartmentData.create_from_department(department)
                    for department in departments
                ],
                "meta": {
                    "order": [department.id for department in departments],
                },
            }
        )


@router.get("", status_code=status.HTTP_200_OK)
def list_departments(body: DepartmentRequest = Depends()) -> DepartmentListResponse:
    departments = get_departments_by_filters(body)

    return DepartmentListResponse.create_from_departments(departments)
