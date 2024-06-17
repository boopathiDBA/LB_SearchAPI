from src.core.user.entities import User
from src.core.user.user_repo import UserRepo, IUserRepo


def get_user_details(user_id: str, user_repo: IUserRepo = UserRepo()) -> User:
    return user_repo.get_user_by_id(user_id)


def get_user_wtid(user_id: str, user_repo: IUserRepo = UserRepo()) -> str:
    return user_repo.get_user_wtid(user_id)
