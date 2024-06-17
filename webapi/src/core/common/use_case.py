from src.core.brand.brand_repo import IBrandRepo
from src.core.common.repository import FriendlyId
from src.core.store.store_repo import IStoreRepo


def get_combined_entity_ids(
    friendly_id: FriendlyId | None,
    entity_ids: set[str] | None,
    repo: IBrandRepo | IStoreRepo,
) -> set[str] | None:
    """
    Combine a FriendlyId and a list of ids into a single set of ids
    Used by top_list use cases
    """
    combined_ids = None
    if friendly_id:
        if _id := repo.get_id_by_friendly_id(friendly_id):
            combined_ids = {_id}
    elif entity_ids:
        combined_ids = entity_ids.copy()
    return combined_ids
