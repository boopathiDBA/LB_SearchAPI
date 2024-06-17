from pydantic import Field, ConfigDict, model_validator

from src.core.common.base_entity import BaseEntity


class UserNotificationSetting(BaseEntity):
    id: int = Field(description="Notification Setting identifier", examples=["94"])
    user_id: int = Field(description="User identifier", examples=["94"])
    global_: bool | None = Field(alias="global", default=None)
    alerts: bool | None = Field(
        description="Notification alerts", default=None
    )  # null,
    popup_count: int = (
        Field(description="Notification Setting popup_count", examples=[2]),
    )
    hide_popup: bool = Field(description="Notification Setting hide_popup")
    favourites_state: str | None = Field(
        description="Notification Setting favourites_state",
        examples=["departmentSelect"],
    )

    model_config = ConfigDict(populate_by_name=True)


class UserDBEntity(BaseEntity):
    """
    This entity only has fields that exist in the 'users' table in the DB.
    Any additional fields must be added to the extended 'User' class defined below.
    """

    id: str = Field(description="User identifier", examples=["94"])

    # This field is required to derive `about_complete` field
    firstname: str | None = Field(description="User's firstname", examples=["John"])
    email: str = Field(description="User's email", examples=["example@gmail.com"])
    followers_count: int | None = Field(
        description="User's followers_count", examples=["100"]
    )
    slug: str = Field(description="User's slug", examples=["john"])
    upvotes_count: int = Field(description="User's upvotes_count", examples=["100"])
    downvotes_count: int = Field(description="User's downvotes_count", examples=["100"])
    username: str | None = Field(description="User's username", examples=["john123"])
    avatar: str | None = Field(
        description="User's image avatar",
        default=None,
    )
    deals_count: int = Field(description="User's deals_count", examples=["100"])
    coupons_count: int = Field(description="User's coupons_count", examples=["100"])
    sale_events_count: int = Field(
        description="User's sale_events_count", examples=["100"]
    )
    impressions_count: int = Field(
        description="User's impressions_count", examples=["100"]
    )
    comments_count: int = Field(description="User's comments_count", examples=["100"])
    upvoted_count: int = Field(description="User's upvoted_count", examples=["100"])
    downvoted_count: int = Field(description="User's downvoted_count", examples=["100"])
    public_profile_settings: dict = Field(description="User's public_profile_settings")
    gender: str | None = Field(description="User's gender", examples=["M", "F"])

    # NOTE: below are commented out as it is not used in the code.
    # Additionally Rails API does not return these fields. This could potentially be a data leak.
    # So I have commented it out. To be on safe side.
    # If needed/uncommented, update the API layer to remove these fields.

    # about: str | None = Field(description="User's about", default=None)
    # dob: str | None = Field(description="User's dob", default=None)
    # location_state: str | None = Field(
    #     description="User's location_state", default=None
    # )
    # role: str = Field(description="User's role", examples=["Admin"])
    # phone_number: str | None = Field(
    #     description="User's phone number", examples=["12-345-6789"], default=None
    # )
    # surname: str | None = Field(description="User's surname", examples=["Doe"])


class User(UserDBEntity):
    about_complete: bool = Field(
        default=False,
        description="Determines if a User has firstname and gender present",
    )

    notification_setting: UserNotificationSetting | None = Field(
        description="User's notification settings", default=None
    )
    hide_popup: bool = Field(default=False, description="User's hide popup")

    # Typing should be same at NotificationSetting.popup_count
    # Value is derived from NotificationSetting.popup_count
    popup_count: int = (
        Field(description="Notification Setting popup_count", examples=[2]),
    )

    # Value is set by validator below
    notification_status: bool | None = Field(
        default=None, description="User's notification status"
    )

    department_followed: bool = Field(
        default=False, description="Does the user follow any department?"
    )
    brand_followed: bool = Field(
        default=False, description="Does the user follow any brand?"
    )
    store_followed: bool = Field(
        default=False, description="Does the user follow any store?"
    )

    @model_validator(mode="after")
    def _maybe_set_about_complete(self) -> "User":

        # using hasattr here as cloner subclasses may not have these fields
        if (
            hasattr(self, "firstname")
            and self.firstname
            and hasattr(self, "gender")
            and self.gender
        ):
            self.about_complete = True
        return self

    @model_validator(mode="after")
    def _set_hide_popup(self) -> "User":
        """Set User `hide_popup` field based on `notification_setting` fields"""
        if self.notification_setting is not None and (
            self.notification_setting.popup_count >= 2
            or self.notification_setting.hide_popup
        ):
            self.hide_popup = True
        return self

    @model_validator(mode="after")
    def _set_popup_count(self) -> "User":
        """Set User `popup_count` field based on `notification_setting` field"""
        if self.notification_setting is not None:
            self.popup_count = self.notification_setting.popup_count
        return self

    @model_validator(mode="after")
    def _maybe_set_nofitication_status(self) -> "User":
        if (
            self.notification_setting is not None
            and self.notification_setting.global_ is not None
        ):
            self.notification_status = self.notification_setting.global_
        else:
            self.notification_status = None
        return self
