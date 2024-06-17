from pydantic import EmailStr
from src.core.braze.entities import BrazeUser
from src.core.braze.braze_repo import BrazeRepo, IBrazeRepo, BrazeMergeUsersRequest


def get_users_by_email(
    email: EmailStr, braze_repo: IBrazeRepo = BrazeRepo()
) -> list[BrazeUser]:
    return braze_repo.get_users_by_email(email)


def get_users_by_external_ids(
    external_ids: list[str], braze_repo: IBrazeRepo = BrazeRepo()
) -> list[BrazeUser]:
    return braze_repo.get_users_by_external_ids(external_ids)


def merge_users_by_external_ids(
    merge_request: BrazeMergeUsersRequest,
    braze_repo: IBrazeRepo = BrazeRepo(),
) -> str:
    """
    This use case enables the merging of users with two different external IDs into a single Braze user.
    When a user accesses the app (whether it's on the backend, web, or mobile) for the first time without logging in,
    a new user is created in Braze with a unique ID. This user is then stored in local storage.
     If the same user later signs up and logs in again, a new user with an email is created in Braze.
     Subsequently, the merge API is invoked to merge both users based on their external IDs
    """
    return braze_repo.merge_users_by_external_ids(merge_request)
