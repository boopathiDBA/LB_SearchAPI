from fastapi import HTTPException, status


class BaseHttpException(HTTPException):
    def __init__(self, status_code: int = None, detail: str = None):
        status_code = status_code or self._DEFAULT_STATUS_CODE
        detail = detail or self._DEFAULT_DETAIL
        super().__init__(status_code, detail)


class NotFoundHttpException(BaseHttpException):
    _DEFAULT_STATUS_CODE = status.HTTP_404_NOT_FOUND
    _DEFAULT_DETAIL = "Not Found"


class UnauthorizedHttpException(BaseHttpException):
    _DEFAULT_STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    _DEFAULT_DETAIL = "Unauthorized"
