from http import HTTPStatus


async def test_auth_health(stats_client):
    response = await stats_client.get("/health")
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["status"] == "ok"
