import os
from enum import Enum
from typing import Protocol

import jwt


class AlgorithmEnum(Enum):
    """Supported Token decoding algorithms"""

    HS256 = "HS256"


class TokenVerificationFailed(Exception):
    """Raise when token verification fails"""

    pass


class IAuthenticator(Protocol):
    """Responsible for Authentication of JWT Tokens"""

    def generate_token(self, payload: dict[str, str]) -> str:
        pass

    def verify_and_decode_token(
        self, token: str, algorithm: AlgorithmEnum = AlgorithmEnum.HS256
    ) -> dict[str, str]:
        """Verify that JWT token is valid and has not been tampered with.

        Raises:
            TokenVerificationFailed: If token verification fails.
        """
        pass


class Authenticator(IAuthenticator):
    def __init__(self, key: str):
        """
        Parameters:
            key: Key string that is used sign JWT tokens. This key is used to encode and decode token.
        """
        self._key = key

    def generate_token(self, payload: dict[str, str]) -> str:
        return jwt.encode(payload, self._key, algorithm=AlgorithmEnum.HS256.value)

    def verify_and_decode_token(
        self, token: str, algorithm: AlgorithmEnum = AlgorithmEnum.HS256
    ) -> dict[str, str]:
        try:
            return jwt.decode(token, self._key, algorithms=[algorithm.value])
        except Exception:
            # TODO logger error
            raise TokenVerificationFailed()


def get_authenticator() -> IAuthenticator:
    return Authenticator(key=os.environ.get("JWT_SIGNING_KEY", "mock_signing_key_str"))
