from uuid import uuid4

from pydantic import Field

from src.common.base_model import BaseModel


class Context(BaseModel):
    """
    Contains contextual data about the request.
    """

    user_id: str | None = Field(
        description="user_id if user is logged in", examples=["1"], default=None
    )
    correlation_id: str = Field(
        default_factory=uuid4,
        description="To be used for logging, ID used to correlate request externally",
    )
    request_id: str = Field(
        default_factory=uuid4,
        description="To be used for logging. Unique for each request",
    )
    client_ip: str | None = Field(
        description="To be used in analytics, ip address of client",
        default=None,
        examples=["127.0.0.1", "172.31.0.5"],
    )
    referrer: str | None = Field(
        description="To be used in analytics, referrer from headers",
        default=None,
        examples=["http://blue.littlebirdie.com/shop/coupon/catch-coupon-test-2"],
    )
