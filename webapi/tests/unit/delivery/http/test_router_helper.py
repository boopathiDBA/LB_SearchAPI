from typing import Callable


from src.core.common.auth import AlgorithmEnum
from src.core.common.auth.authenticator import (
    IAuthenticator,
    TokenVerificationFailed,
    get_authenticator,
)
from src.delivery.http.http_exceptions import (
    NotFoundHttpException,
    UnauthorizedHttpException,
)
from src.delivery.http.router_helper import authenticated_route, Request
import pytest


class _MockAuthenticator(IAuthenticator):
    def __init__(self, verify_decode_token_func: Callable = None):
        self._verity_decode_token_func = verify_decode_token_func or (lambda x: None)

    def generate_token(self, payload: dict[str, str]) -> str:
        return ""

    def verify_and_decode_token(
        self, token: str, algorithm: AlgorithmEnum = AlgorithmEnum.HS256
    ) -> dict[str, str]:
        return self._verity_decode_token_func()


def _mock_verify_decode_token_func():
    raise TokenVerificationFailed


_mock_authenticator = _MockAuthenticator(
    verify_decode_token_func=_mock_verify_decode_token_func
)


def _get_mock_request(headers: list[tuple[bytes, bytes]] = None) -> Request:
    headers = headers or {}
    return Request(scope={"type": "http", "headers": headers})


def test_authenticate_route_sets_context_to_request_with_valid_token():
    authenticator = get_authenticator()
    auth_token = authenticator.generate_token({"user_id": "999"})
    request = _get_mock_request(
        headers=[(b"x-auth-token", auth_token.encode("latin-1"))]
    )

    @authenticated_route(authenticator=authenticator)
    def mock_route(request: Request = None) -> bool:
        return True

    assert mock_route(request=request) is True
    assert request.context
    assert request.context.user_id == "999"


def test_authenticate_route_raises_error_with_request_without_authorization_header():
    @authenticated_route
    def mock_route(request: Request = None) -> bool:
        return True

    with pytest.raises(NotFoundHttpException):
        mock_route(request=_get_mock_request(headers=[]))


def test_authenticate_route_raises_error_with_invalid_token():
    @authenticated_route
    def mock_route(request: Request = None) -> bool:
        return True

    with pytest.raises(UnauthorizedHttpException):
        mock_route(
            request=_get_mock_request(
                headers=[(b"x-auth-token", b"Bearer invalid_token")]
            )
        )


def test_authenticate_route_raises_with_skip_verification_with_token():
    """When skip_verification is set to True and a token is passed into request, then token should be verified."""

    @authenticated_route(
        skip_verification_if_no_token=True, authenticator=_mock_authenticator
    )
    def mock_route(request: Request = None) -> bool:
        return True

    with pytest.raises(UnauthorizedHttpException):
        mock_route(
            request=_get_mock_request(
                headers=[(b"x-auth-token", b"Bearer invalid_token")]
            )
        )


def test_authenticate_route_returns_with_skip_verification_with_without_token():
    """When skip_verification is set to True and a token is not passed into request.
    Then authenticator should not raise."""

    @authenticated_route(skip_verification_if_no_token=True)
    def mock_route(request: Request = None) -> bool:
        return True

    assert mock_route(request=_get_mock_request(headers=[])) is True
