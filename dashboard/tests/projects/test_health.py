from http import HTTPStatus


async def test_auth_health(projects_client):
    response = await projects_client.get("/health")
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert data["status"] == "ok"
