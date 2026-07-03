def test_root(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Pytex!"}


def test_ping(client):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
