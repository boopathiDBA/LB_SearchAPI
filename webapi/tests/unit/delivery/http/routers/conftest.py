import pytest
from src.adapters import rds_client


@pytest.fixture(autouse=True)
def monkey_patch_db_connection(monkeypatch):
    """
    Fixture expected to be used for all router tests.
    This is required as currently our app makes a db connection on start up.
    We don't need any connection for router testing therefore, we monkey patch to avoid the db connection.
    An assumption is made that all router testing shouldn't reach any of the lower layer code
    therefore the mock method just returns a boolean true.
    """

    def mock_init_rds_client():
        return True

    monkeypatch.setattr(rds_client, "get_initialised_rds_client", mock_init_rds_client)


@pytest.fixture()
def monkey_patch_get_top_brands(monkeypatch):
    from src.core.brand import use_case

    def mock_get_top_brands(*args, **kwargs):
        return []

    monkeypatch.setattr(use_case, "get_top_brands", mock_get_top_brands)


@pytest.fixture()
def monkey_patch_get_top_vouchers(monkeypatch):
    from src.core.voucher import use_case

    def mock_get_top_vouchers(*args, **kwargs):
        return []

    monkeypatch.setattr(use_case, "get_top_vouchers", mock_get_top_vouchers)


@pytest.fixture()
def test_client(
        monkey_patch_get_top_brands,
        monkey_patch_get_top_vouchers
):
    from src.delivery.http.main import app
    from starlette.testclient import TestClient

    return TestClient(app)
