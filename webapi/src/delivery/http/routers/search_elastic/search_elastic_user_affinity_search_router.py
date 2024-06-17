from fastapi import APIRouter, status

from src.common.base_model import BaseModel
from src.core.common.user_affinity.user_affinity_request import UserAffinityRequest
from src.core.sale_event.entities import ElasticSearchUserAffinitySaleEvent
from src.core.sale_event.use_case import get_user_affinity_sale_events
from src.core.voucher.entities import ElasticSearchUserAffinityVoucher
from src.core.voucher.use_case import get_user_affinity_vouchers

router = APIRouter()


class UserAffinityResponse(BaseModel):
    # Currently deals are not supported. But we return empty list to not cause issues for front end.
    deals: list = []
    vouchers: list[ElasticSearchUserAffinityVoucher] = []
    sale_events: list[ElasticSearchUserAffinitySaleEvent] = []


@router.post("/user_affinity_search", status_code=status.HTTP_200_OK)
def user_affinity_search(body: UserAffinityRequest) -> UserAffinityResponse:
    """Return vouchers and sale_events based on user's affinity.

    The affinity is defined in the payload. It is assumed that the affinity data is
    retrieved with another API call: /api/elastic_search/affinity.

    Note: Currently `deals` data is deprecated and is no longer supported.
    But we return empty list to not cause issues for front end.

    Note. In the previous rails application there was logic to allow for personalisation overrides which allow,
    for admin configuration to override results. This feature used the table "personalisation_override"
    and "personalisation_override_items". We have chosen to not implement these features as part of the
    migration as the tables have not been in use for a long time and the feature is not used by the business.
    See ticket for the discussion: https://littlebirdie.atlassian.net/browse/API-1251
    """
    sale_events = get_user_affinity_sale_events(body)
    vouchers = get_user_affinity_vouchers(body)

    return UserAffinityResponse(sale_events=sale_events, vouchers=vouchers)
