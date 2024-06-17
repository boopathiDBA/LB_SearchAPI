from fastapi import status, APIRouter

from src.common.base_model import BaseModel
from src.common.string_utils import pascal_case_to_snake_case
from src.core.custom_widget.entities import (
    CustomWidgetDBEntity,
    CustomWidgetPositionEnum,
    CustomWidgetItemTypeEnum,
    CustomWidgetItem,
)
from src.core.custom_widget.usecase import get_custom_widget, GetCustomWidgetResponse
from src.core.sale_event.entities import SaleEvent
from src.core.voucher.entities import Voucher
from src.delivery.http.routers.common.responses import (
    SaleEventResponseAttributes,
    SaleEventResponseObject,
    VoucherResponseAttributes,
    VoucherResponseObject,
)

router = APIRouter(prefix="/custom_widgets")


CURRENTLY_SUPPORTED_ITEM_TYPES = [
    CustomWidgetItemTypeEnum.VOUCHER,
    CustomWidgetItemTypeEnum.SALE_EVENT,
]


class CustomWidgetAttributesWithItem(BaseModel):
    item: VoucherResponseAttributes | SaleEventResponseAttributes

    @classmethod
    def create(cls, item: Voucher | SaleEvent) -> "CustomWidgetAttributesWithItem":
        return cls.model_validate({"item": dict(item)})


class CustomWidgetItemRelationshipItemData(BaseModel):
    id: str
    type: str


class CustomWidgetItemRelationshipItem(BaseModel):
    data: CustomWidgetItemRelationshipItemData


class CustomWidgetItemRelationships(BaseModel):
    item: CustomWidgetItemRelationshipItem


class CustomWidgetItemResponseData(BaseModel):
    id: str
    type: str = "custom_widget_item"
    attributes: CustomWidgetAttributesWithItem
    relationships: CustomWidgetItemRelationships

    @classmethod
    def create(
        cls,
        item: CustomWidgetItem,
        items_by_id_type: dict[(str, str), Voucher | SaleEvent],
    ) -> "CustomWidgetItemResponseData":

        return cls.model_validate(
            {
                "id": item.item_id,
                "attributes": CustomWidgetAttributesWithItem.create(
                    items_by_id_type[(item.item_id, item.item_type)]
                ),
                "relationships": {
                    "item": {
                        "data": {
                            "id": item.item_id,
                            "type": pascal_case_to_snake_case(item.item_type),
                        }
                    }
                },
            }
        )


class CustomWidgetMergedResponse(BaseModel):
    data: list[CustomWidgetItemResponseData]
    included: list[VoucherResponseObject | SaleEventResponseObject]

    @classmethod
    def _map_item_id_and_type_to_item(
        cls,
        custom_widget_response: GetCustomWidgetResponse,
    ) -> dict[(str, str), Voucher | SaleEvent]:

        # Hash tables of entities by their id
        sale_events_mapping = {
            item.id: item for item in custom_widget_response.sale_events
        }
        vouchers_mapping = {item.id: item for item in custom_widget_response.vouchers}

        map = {}
        for item in custom_widget_response.custom_widget.items:
            found_item = None

            if item.item_type == CustomWidgetItemTypeEnum.SALE_EVENT:
                found_item = sale_events_mapping[item.item_id]
            elif item.item_type == CustomWidgetItemTypeEnum.VOUCHER:
                found_item = vouchers_mapping[item.item_id]

            if found_item:
                map[(item.item_id, item.item_type)] = found_item
        return map

    @classmethod
    def create(
        cls, custom_widget_response: GetCustomWidgetResponse
    ) -> "CustomWidgetMergedResponse":
        items_mapping = cls._map_item_id_and_type_to_item(custom_widget_response)

        data = []
        included = []
        for item in custom_widget_response.custom_widget.items:
            if item.item_type not in CURRENTLY_SUPPORTED_ITEM_TYPES:
                # NOTE:  for some reason there is currently some deals in custom widgets that
                # should not be there. If we encounter such a deal, we should skip usual logic.
                continue

            item_entity = items_mapping[(item.item_id, item.item_type)]

            data.append(CustomWidgetItemResponseData.create(item, items_mapping))

            if item.item_type == CustomWidgetItemTypeEnum.VOUCHER:
                included.append(VoucherResponseObject.create_from_voucher(item_entity))
            else:
                included.append(
                    SaleEventResponseObject.create_from_sale_event(item_entity)
                )

        return cls.model_validate({"data": data, "included": included})


class CustomWidgetItemsResponse(BaseModel):
    id: str
    type: str = "custom_widget"
    attributes: CustomWidgetDBEntity
    items: CustomWidgetMergedResponse

    @classmethod
    def create(
        cls, custom_widget_response: GetCustomWidgetResponse
    ) -> "CustomWidgetItemsResponse":
        return cls.model_validate(
            {
                "id": custom_widget_response.custom_widget.id,
                "attributes": custom_widget_response.custom_widget,
                "items": CustomWidgetMergedResponse.create(custom_widget_response),
            }
        )


class CustomWidgetResponse(BaseModel):
    # NOTE: CustomWidgetResponse should always be empty or single element
    # it is typed as a list to be consistent with Rails API
    data: list[CustomWidgetItemsResponse]

    @classmethod
    def create(
        cls, custom_widget_response: GetCustomWidgetResponse | None
    ) -> "CustomWidgetResponse":
        if custom_widget_response is None:
            return cls.model_validate({"data": []})
        else:
            return cls.model_validate(
                {"data": [CustomWidgetItemsResponse.create(custom_widget_response)]}
            )


@router.get("", status_code=status.HTTP_200_OK)
def get_custom_widget_items_by_position(
    by_position: CustomWidgetPositionEnum,
) -> CustomWidgetResponse:
    custom_widget_response = get_custom_widget(by_position)

    if custom_widget_response is None:
        return CustomWidgetResponse.model_validate({"data": []})
    else:
        return CustomWidgetResponse.create(custom_widget_response)
