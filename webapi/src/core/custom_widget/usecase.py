from pydantic import Field

from src.common.base_model import BaseModel
from src.core.custom_widget.custom_widget_repo import (
    ICustomWidgetRepo,
    CustomWidgetRepo,
)
from src.core.custom_widget.entities import (
    CustomWidgetPositionEnum,
    CustomWidgetItem,
    CustomWidget,
    CustomWidgetItemTypeEnum,
)
from src.core.sale_event.entities import SaleEvent
from src.core.sale_event.sale_event_repo import ISaleEventRepo, SaleEventRepo
from src.core.voucher.entities import Voucher
from src.core.voucher.voucher_repo import IVoucherRepo, VoucherRepo


class GetCustomWidgetResponse(BaseModel):
    custom_widget: CustomWidget
    sale_events: list[SaleEvent]
    vouchers: list[Voucher]


def get_custom_widget(
    by_position: CustomWidgetPositionEnum,
    custom_widget_repo: ICustomWidgetRepo = CustomWidgetRepo(),
    vouchers_repo: IVoucherRepo = VoucherRepo(),
    sale_events_repo: ISaleEventRepo = SaleEventRepo(),
) -> GetCustomWidgetResponse | None:
    custom_widget = custom_widget_repo.get_custom_widget(by_position)

    if not custom_widget:
        return None

    # Fetch vouchers if custom widget contains any voucher items else set it to empty list
    voucher_ids = _get_item_ids(custom_widget.items, CustomWidgetItemTypeEnum.VOUCHER)
    vouchers = vouchers_repo.get_by_ids(voucher_ids) if voucher_ids else []

    # Fetch sale events if custom widget contains any sale items else set it to empty list
    sale_event_ids = _get_item_ids(
        custom_widget.items, CustomWidgetItemTypeEnum.SALE_EVENT
    )
    sale_events = sale_events_repo.get_by_ids(sale_event_ids) if sale_event_ids else []

    response = GetCustomWidgetResponse.model_validate(
        {
            "custom_widget": custom_widget,
            "vouchers": vouchers,
            "sale_events": sale_events,
        }
    )
    return response


def _get_item_ids(items: list[CustomWidgetItem], item_type: str) -> list[str]:
    """Get IDs of items with the given item type."""
    return [str(item.item_id) for item in items if item.item_type == item_type]
