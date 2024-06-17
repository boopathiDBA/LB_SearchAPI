from starlette.testclient import TestClient


def test_top_lists_vouchers_invalid_order_by_column(test_client: TestClient):
    response = test_client.get(
        "/api/top_lists/coupons", params={"by_order[column]": "fixed_global_scores"}
    )
    assert response.status_code == 422

    response = test_client.get(
        "/api/top_lists/coupons", params={"by_order[column]": "ranked"}
    )
    assert response.status_code == 422

    response = test_client.get(
        "/api/top_lists/coupons", params={"by_order[column]": "brand_name"}
    )
    assert response.status_code == 422
