import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.monitoring import maybe_setup_sentry
from src.common.logging import setup_logging

from .routers.auth_router import router as auth_router
from .routers.brand_router import router as brand_router
from .routers.categories_router import router as categories_router
from .routers.departments_router import router as departments_router
from .routers.experiment_router import router as experiment_router
from .routers.root_router import router as root_router
from .routers.search_elastic import router as search_elastic_router
from .routers.store_router import router as store_router
from .routers.users_router import router as user_router
from .routers.top_lists_router import router as top_lists_router
from .routers.cba_offer_router import router as cba_offer_router
from .routers.voucher_router import router as voucher_router
from .routers.marketing_router import router as marketing_router
from .routers.todays_top_picks_router import router as todays_top_picks_router
from .routers.custom_widget_router import router as custom_widget_router
from .routers.braze_router import router as braze_router


# `app` is expected to be defined in this module by the ASGI server.
app = FastAPI()

maybe_setup_sentry()

setup_logging()

# CORS configuration
origins = [
    "https://www.littlebirdie.com.au",
    "https://rapp.littlebirdie.com.au",
]

dev_origins = ["https://littlebirdie.dev", "http://localhost", "http://127.0.0.1"]

if os.getenv("DEPLOY_ENV") == "uat":
    origins.extend(dev_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

routers = [
    root_router,
    auth_router,
    search_elastic_router,
    categories_router,
    departments_router,
    brand_router,
    store_router,
    user_router,
    top_lists_router,
    cba_offer_router,
    experiment_router,
    voucher_router,
    marketing_router,
    todays_top_picks_router,
    custom_widget_router,
    braze_router,
]


for router in routers:
    app.include_router(router, prefix="/api")
