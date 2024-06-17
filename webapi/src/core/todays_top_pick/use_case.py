from src.core.todays_top_pick.todays_top_pick_repo import (
    ITodaysTopPickRepo,
    TodaysTopPickRepo,
)
from src.core.todays_top_pick.entities import TodaysTopPick


def get_todays_top_pick(
    todays_top_pick_repo: ITodaysTopPickRepo = TodaysTopPickRepo(),
) -> list[TodaysTopPick]:
    return todays_top_pick_repo.get_todays_top_picks()
