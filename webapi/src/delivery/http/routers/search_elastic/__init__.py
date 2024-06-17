from fastapi import APIRouter

from .search_elastic_affinity_router import router as search_elastic_affinity_router
from .search_elastic_filter_options_router import (
    router as search_elastic_filter_options_router,
)
from .search_elastic_global_suggestions_router import (
    router as search_elastic_global_suggestions_router,
)
from .search_elastic_sale_events_router import (
    router as search_elastic_sale_events_router,
)
from .search_elastic_user_affinity_search_router import (
    router as search_elastic_user_affinity_search_router,
)
from .search_elastic_vouchers_router import router as search_elastic_vouchers_router

router = APIRouter(prefix="/search_elastic")

router.include_router(search_elastic_affinity_router)
router.include_router(search_elastic_filter_options_router)
router.include_router(search_elastic_global_suggestions_router)
router.include_router(search_elastic_vouchers_router)
router.include_router(search_elastic_sale_events_router)
router.include_router(search_elastic_user_affinity_search_router)
