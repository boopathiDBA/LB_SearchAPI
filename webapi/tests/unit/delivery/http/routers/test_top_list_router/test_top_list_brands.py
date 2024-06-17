from starlette.testclient import TestClient


def test_top_lists_brands_invalid_page(test_client: TestClient):
    response = test_client.get("/api/top_lists/brands", params={"page": 0})
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be greater than or equal to 1"
    )


def test_top_lists_brands_invalid_per_page(test_client: TestClient):
    response = test_client.get("/api/top_lists/brands", params={"per_page": -1})
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be greater than or equal to 1"
    )

    response = test_client.get("/api/top_lists/brands", params={"per_page": 1000})
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be less than or equal to 50"
    )


def test_top_lists_brands_invalid_order_by_column(test_client: TestClient):
    response = test_client.get(
        "/api/top_lists/brands", params={"by_order[column]": "department"}
    )
    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Input should be 'name', 'rank' or 'deals_count'"
    )


def test_top_lists_brands_invalid_order_by_direction(test_client: TestClient):
    response = test_client.get(
        "/api/top_lists/brands", params={"by_order[direction]": "descending"}
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be 'asc' or 'desc'"


def test_top_lists_brands_valid_order_by_direction(test_client: TestClient):
    response = test_client.get(
        "/api/top_lists/brands", params={"by_order[direction]": "asc"}
    )
    assert response.status_code == 200

    response = test_client.get(
        "/api/top_lists/brands", params={"by_order[direction]": "ASC"}
    )
    assert response.status_code == 200

    response = test_client.get(
        "/api/top_lists/brands", params={"by_order[direction]": "deSC"}
    )
    assert response.status_code == 200
