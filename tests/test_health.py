def test_health_code(client):
    response = client.get("/test")
    assert response.status_code == 200


def test_health_response(client):
    response = client.get("/test")
    assert response.json() == "Success"
