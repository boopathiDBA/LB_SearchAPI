import pytest

from src.core.common.auth import Authenticator, TokenVerificationFailed

_MOCK_SECRET: str = "very_important_mock_secret"
_MOCK_CLAIMS = {"some_key": "some_value"}


def _get_mock_authenticator(key: str = _MOCK_SECRET) -> Authenticator:
    return Authenticator(key=key)


def test_verification_of_valid_token_generated_from_same_secret() -> None:
    """Verification should pass if token is signed and verified against the same key"""
    authenticator = _get_mock_authenticator()
    token = authenticator.generate_token(_MOCK_CLAIMS)
    assert authenticator.verify_and_decode_token(token)


def test_raises_with_token_signed_with_different_key() -> None:
    """Verification should fail if token is signed and verified against different keys"""
    authenticator = _get_mock_authenticator(key="a_different_key")
    token = authenticator.generate_token(_MOCK_CLAIMS)

    with pytest.raises(TokenVerificationFailed):
        _get_mock_authenticator().verify_and_decode_token(token)


def test_raises_with_modified_token() -> None:
    """If a valid token is tampered with, verification should fail"""
    authenticator = _get_mock_authenticator()
    valid_token = authenticator.generate_token(_MOCK_CLAIMS)
    authenticator.verify_and_decode_token(valid_token)

    modified_chars = "QWERTY"
    modified_token = modified_chars + valid_token[len(modified_chars) :]

    with pytest.raises(TokenVerificationFailed):
        authenticator.verify_and_decode_token(modified_token)
