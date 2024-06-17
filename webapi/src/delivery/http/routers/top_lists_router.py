from typing import Annotated

from fastapi import APIRouter, Query
from fastapi import status
from pydantic import Field

from src.common.base_model import BaseModel
from src.core.brand.use_case import (
    get_top_brands,
    get_top_brands_followed_by_user,
    get_top_brands_by_department,
    TopBrandsOrderColumnEnum,
    TOP_BRANDS_DEFAULT_ORDER,
    get_top_brands_by_store,
)
from src.core.common.repository import Page, Order, FriendlyId, TOP_LIST_DEFAULT_PAGE
from src.core.sale_event.entities import SaleEvent
from src.core.sale_event.use_case import (
    TopSaleEventsOrderColumnEnum,
    TOP_SALE_EVENTS_DEFAULT_ORDER,
    get_top_sale_events,
)
from src.core.store.store_repo import IStoreRepo, StoreRepo
from src.core.store.use_case import (
    TopStoresOrderColumnEnum,
    TOP_STORES_DEFAULT_ORDER,
    get_top_stores,
)
from src.core.voucher.entities import Voucher
from src.core.voucher.use_case import (
    TOP_VOUCHERS_DEFAULT_ORDER,
    get_top_vouchers,
    TopVouchersOrderColumnEnum,
)
from src.delivery.http.router_helper import authenticated_route, Request
from src.delivery.http.routers.brand_router import BrandListResponse
from src.delivery.http.routers.common.params import (
    PageNumberQueryParam,
    PerPageQueryParam,
    OrderByDirectionQueryParam,
)
from src.delivery.http.routers.common.responses import (
    SaleEventResponseObject,
    ListResponseMeta,
    VoucherResponseObject,
)
from src.delivery.http.routers.store_router import (
    StoreResponseObject,
    StoreListResponse,
)

router = APIRouter(prefix="/top_lists")

DepartmentFriendlyIdQueryParam = Annotated[
    FriendlyId | None,
    Query(
        description="Unique identifier like an id or slug of a Department",
        examples=["appliances", "fashion"],
    ),
]
DepartmentIdsQueryParam = Annotated[
    set[str] | None,
    Query(description="List of department ids", alias="by_departments[]"),
]
CategoryFriendlyIdQueryParam = Annotated[
    FriendlyId | None,
    Query(
        description="Unique identifier like an id or slug of a Category",
        examples=["cookware"],
    ),
]
CategoryIdsQueryParam = Annotated[
    set[str] | None,
    Query(description="List of category ids", alias="by_categories[]"),
]
StoreFriendlyIdQueryParam = Annotated[
    FriendlyId | None,
    Query(
        description="Unique identifier like an id or slug of a Store",
        examples=["kmart"],
    ),
]
StoreIdsQueryParam = Annotated[
    set[str] | None, Query(description="List of store ids", alias="by_stores[]")
]
BrandFriendlyIdQueryParam = Annotated[
    FriendlyId | None,
    Query(
        description="Unique identifier like an id or slug of a Brand",
        examples=["adidas"],
    ),
]
BrandIdsQueryParam = Annotated[
    set[str] | None, Query(description="List of brand ids", alias="by_brands[]")
]


@router.get("/brands", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def top_brands_list(
    request: Request,
    page: PageNumberQueryParam = TOP_LIST_DEFAULT_PAGE.page_number,
    per_page: PerPageQueryParam = TOP_LIST_DEFAULT_PAGE.per_page,
    order_by_column: Annotated[
        TopBrandsOrderColumnEnum | None,
        Query(alias="by_order[column]", examples=TopBrandsOrderColumnEnum.NAME),
    ] = TOP_BRANDS_DEFAULT_ORDER.column,
    order_by_direction: OrderByDirectionQueryParam = TOP_BRANDS_DEFAULT_ORDER.direction,
    by_department: DepartmentFriendlyIdQueryParam = None,
    by_store: StoreFriendlyIdQueryParam = None,
    by_followed_user: Annotated[str | None, Query(examples="1234")] = None,
) -> BrandListResponse:
    page = Page(page_number=page, per_page=per_page)
    order = Order(column=order_by_column, direction=order_by_direction)

    if by_department:
        brands = get_top_brands_by_department(
            department_friendly_id=by_department,
            page=page,
            order=order,
            context=request.context,
        )
    elif by_store:
        brands = get_top_brands_by_store(
            store_friendly_id=by_store,
            page=page,
            order=order,
            context=request.context,
        )
    elif by_followed_user:
        brands = get_top_brands_followed_by_user(
            user_id=by_followed_user, page=page, order=order
        )
    else:
        brands = get_top_brands(page=page, order=order, context=request.context)
    return BrandListResponse.create_from_brands(brands)


class SaleEventListResponse(BaseModel):
    data: list[SaleEventResponseObject] = Field(
        default=[], description="List of sale events"
    )
    meta: ListResponseMeta = Field(
        default_factory=ListResponseMeta, description="Contains meta data like order"
    )

    @classmethod
    def create_from_sale_events(
        cls, sale_events: list[SaleEvent]
    ) -> "SaleEventListResponse":
        """Factory method to create sale event list response object from sale events"""
        return cls.model_validate(
            {
                "data": [
                    SaleEventResponseObject.create_from_sale_event(sale_event)
                    for sale_event in sale_events
                ],
                "meta": {"order": [int(sale_event.id) for sale_event in sale_events]},
            }
        )


@router.get("/sale_events", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def top_sale_events_list(
    request: Request,
    page: PageNumberQueryParam = TOP_LIST_DEFAULT_PAGE.page_number,
    per_page: PerPageQueryParam = TOP_LIST_DEFAULT_PAGE.per_page,
    order_by_column: Annotated[
        TopSaleEventsOrderColumnEnum | None,
        Query(
            alias="by_order[column]",
            examples=TopSaleEventsOrderColumnEnum.RANK,
        ),
    ] = TOP_SALE_EVENTS_DEFAULT_ORDER.column,
    order_by_direction: OrderByDirectionQueryParam = TOP_SALE_EVENTS_DEFAULT_ORDER.direction,
    by_department: DepartmentFriendlyIdQueryParam = None,
    by_departments: DepartmentIdsQueryParam = None,
    by_category: CategoryFriendlyIdQueryParam = None,
    by_categories: CategoryIdsQueryParam = None,
    by_store: StoreFriendlyIdQueryParam = None,
    by_stores: StoreIdsQueryParam = None,
    by_brand: BrandFriendlyIdQueryParam = None,
    by_brands: BrandIdsQueryParam = None,
    current: Annotated[
        bool | None, Query(description="Filter by ongoing sale events")
    ] = None,
    upcoming: Annotated[
        bool | None, Query(description="Filter by future sale events")
    ] = None,
    by_followed_user: Annotated[
        str | None,
        Query(
            description="Filter by stores followed by the user id/slug",
            examples=["1050", "webapi-automated-test-user-uat"],
        ),
    ] = None,
) -> SaleEventListResponse:
    page = Page(page_number=page, per_page=per_page)
    order = Order(column=order_by_column, direction=order_by_direction)

    sale_events = get_top_sale_events(
        page=page,
        order=order,
        by_department=by_department,
        by_departments=by_departments,
        by_category=by_category,
        by_categories=by_categories,
        by_store=by_store,
        by_stores=by_stores,
        by_brand=by_brand,
        by_brands=by_brands,
        current=current,
        upcoming=upcoming,
        by_followed_user=by_followed_user,
    )
    return SaleEventListResponse.create_from_sale_events(sale_events)


class VoucherListResponse(BaseModel):
    data: list[VoucherResponseObject] = Field(
        default=[], description="List of vouchers"
    )
    included: list[StoreResponseObject]
    meta: ListResponseMeta = Field(
        default_factory=ListResponseMeta, description="Contains meta data like order"
    )

    @classmethod
    def create_from_vouchers(
        cls, vouchers: list[Voucher], store_repo: IStoreRepo = StoreRepo()
    ) -> "VoucherListResponse":
        """Factory method to create voucher list response object from vouchers"""
        store_ids = [voucher.store_id for voucher in vouchers if voucher.store_id]
        stores = store_repo.get_by_ids(store_ids)
        return cls.model_validate(
            {
                "data": [
                    VoucherResponseObject.create_from_voucher(voucher)
                    for voucher in vouchers
                ],
                "included": [
                    StoreResponseObject.create_from_store(store) for store in stores
                ],
                "meta": {"order": [int(voucher.id) for voucher in vouchers]},
            }
        )


@router.get("/coupons", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def top_coupons_list(
    request: Request,
    page: PageNumberQueryParam = TOP_LIST_DEFAULT_PAGE.page_number,
    per_page: PerPageQueryParam = TOP_LIST_DEFAULT_PAGE.per_page,
    order_by_column: Annotated[
        TopVouchersOrderColumnEnum | None,
        Query(
            alias="by_order[column]",
            examples="rank",
        ),
    ] = TOP_VOUCHERS_DEFAULT_ORDER.column,
    order_by_direction: OrderByDirectionQueryParam = TOP_VOUCHERS_DEFAULT_ORDER.direction,
    by_department: DepartmentFriendlyIdQueryParam = None,
    by_departments: DepartmentIdsQueryParam = None,
    by_category: CategoryFriendlyIdQueryParam = None,
    by_categories: CategoryIdsQueryParam = None,
    by_store: StoreFriendlyIdQueryParam = None,
    by_stores: StoreIdsQueryParam = None,
    by_brand: BrandFriendlyIdQueryParam = None,
    by_brands: BrandIdsQueryParam = None,
    by_coupon_types: Annotated[
        list[str] | None,
        Query(
            alias="by_coupon_types[]", description="List of coupon types to filter by"
        ),
    ] = None,
    by_followed_user: Annotated[
        str | None,
        Query(
            description="Filter by stores followed by the user id/slug",
            examples=["1050", "webapi-automated-test-user-uat"],
        ),
    ] = None,
) -> VoucherListResponse:
    page = Page(page_number=page, per_page=per_page)
    order = Order(column=order_by_column, direction=order_by_direction)

    vouchers = get_top_vouchers(
        page=page,
        order=order,
        by_department=by_department,
        by_departments=by_departments,
        by_category=by_category,
        by_categories=by_categories,
        by_store=by_store,
        by_stores=by_stores,
        by_brand=by_brand,
        by_brands=by_brands,
        by_coupon_types=by_coupon_types,
        by_followed_user=by_followed_user,
    )
    return VoucherListResponse.create_from_vouchers(vouchers)


@router.get("/stores", status_code=status.HTTP_200_OK)
@authenticated_route(skip_verification_if_no_token=True)
def top_stores_list(
    request: Request,
    page: PageNumberQueryParam = TOP_LIST_DEFAULT_PAGE.page_number,
    per_page: Annotated[
        int | None, Query(ge=1, le=200)  # Maximum here is different to the usual 50
    ] = TOP_LIST_DEFAULT_PAGE.per_page,
    order_by_column: Annotated[
        TopStoresOrderColumnEnum | None,
        Query(
            alias="by_order[column]",
            examples="rank",
        ),
    ] = TOP_STORES_DEFAULT_ORDER.column,
    order_by_direction: OrderByDirectionQueryParam = TOP_STORES_DEFAULT_ORDER.direction,
    by_department: DepartmentFriendlyIdQueryParam = None,
    by_followed_user: Annotated[
        FriendlyId | None,
        Query(
            description="Filter by stores followed by the user friendly id",
            examples="1050",
        ),
    ] = None,
) -> StoreListResponse:
    page = Page(page_number=page, per_page=per_page)
    order = Order(column=order_by_column, direction=order_by_direction)

    stores = get_top_stores(
        page=page,
        order=order,
        by_department=by_department,
        by_followed_user=by_followed_user,
    )
    return StoreListResponse.create_from_stores(stores)
