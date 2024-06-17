import os
import logging
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

logger = logging.getLogger(__name__)


def maybe_setup_sentry():
    """Set up Sentry for application.

    Sentry is a service we use for alerting.
    """

    # Only set up sentry for Production and UAT environments
    if (environment := os.getenv("DEPLOY_ENV")) not in ["prod", "uat"]:
        return

    # If SENTRY_DSN is not set, do not set up Sentry
    if (dsn := os.getenv("SENTRY_DSN")) is None:
        logger.error(
            "SENTRY_DSN not set in environment variables. Sentry will not be set up."
        )
        return

    sentry_logging = LoggingIntegration(
        level=logging.DEBUG,  # Capture debug and above as breadcrumbs
        event_level=logging.WARN,  # Send warnings, error, critical logs as events
    )

    # Only sample 10% of transactions in production, other environments are 0%
    traces_sample_rate = 0.1 if environment == "prod" else 0.0

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            sentry_logging,
        ],
        environment=environment,
        # Set traces_sample_rate to 1.0 to capture 100% of transactions for performance monitoring.
        traces_sample_rate=traces_sample_rate,
        # Set profiles_sample_rate to 1.0 to profile 100% of sampled transactions.
        # It is not recommended for have 100% profiling in production.
        profiles_sample_rate=1.0,
    )
