import functools
import os

from fastapi import Request as FastapiRequest

from src.core.common.auth.authenticator import (
    get_authenticator,
    TokenVerificationFailed,
    IAuthenticator,
)
from src.core.common.context import Context
from src.delivery.http.http_exceptions import (
    NotFoundHttpException,
    UnauthorizedHttpException,
)

IMAGE_BASE_URL = os.getenv(
    "IMAGE_BASE_URL",
    "https://project-deals-staging.s3.ap-southeast-2.amazonaws.com/uploads",
)


class Request(FastapiRequest):
    context: Context


def _ensure_request_parameter_is_configured(kwargs: dict[str, any]) -> None:
    if "request" not in kwargs:
        raise Exception(
            f"Unable to find `request` argument. To use decorator `authenticated_route` the decorated function "
            f"requires the parameter `request: Request`."
        )


def _get_and_verify_token_claims(
    token: str,
    authenticator: IAuthenticator,
) -> dict[str, any]:
    try:
        return authenticator.verify_and_decode_token(token)
    except TokenVerificationFailed:
        raise UnauthorizedHttpException()


def authenticated_route(
    _func=None,
    *,
    skip_verification_if_no_token: bool = False,
    authenticator: IAuthenticator = get_authenticator(),
):
    """
    Decorator ensures incoming JWT token is valid.

    To use this decorator:
        1. Place on top of your router function and below the FastAPI decorator.
        2. Ensure that there is a kwarg named `request` as a parameter.
            eg.
                 @router.get("/myroute")
                 @authenticator
                 def myroute(request: Request:
                     pass

    A side effect of this decorator is the incoming `request` argument has a context attached to it. The Context object
    will contain `user`. Example usage: `request.context.user.id`

    Parameters:
        skip_verification_if_no_token:  Determines if the route will allow for request that do not
                                        contain the auth header. When this is False no authentication is performed,
                                        however, if a token is supplied it is performed.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(
            *args,
            **kwargs,
        ):
            _ensure_request_parameter_is_configured(kwargs)

            context_args = {}

            if (
                x_auth_token := kwargs["request"].headers.get("x-auth-token")
            ) is None and skip_verification_if_no_token is False:
                raise NotFoundHttpException()

            if x_auth_token:
                claims = _get_and_verify_token_claims(x_auth_token, authenticator)
                # TODO: verify that user_id is valid with database. Should leverage some caching.
                # TODO: Ensure token is invalid if use has logged out.
                context_args["user_id"] = str(claims["user_id"])
                context_args["referrer"] = kwargs["request"].headers.get("referer")
                if kwargs["request"].client:
                    context_args["client_ip"] = kwargs["request"].client.host
            kwargs["request"].context = Context(**context_args)
            res = func(*args, **kwargs)

            return res

        return wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)
