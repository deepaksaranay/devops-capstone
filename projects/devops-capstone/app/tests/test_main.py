import pytest

from main import MemoryStore, create_app


class BrokenStore(MemoryStore):
    def ping(self):
        raise RuntimeError("database down")


@pytest.fixture
def client():
    return create_app(MemoryStore()).test_client()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_ready_ok(client):
    assert client.get("/ready").status_code == 200


def test_ready_fails_when_store_is_down():
    client = create_app(BrokenStore()).test_client()
    assert client.get("/ready").status_code == 503


def test_items_start_empty(client):
    assert client.get("/items").get_json() == []


def test_add_and_list_items(client):
    created = client.post("/items", json={"name": "laptop"})
    assert created.status_code == 201
    assert created.get_json() == {"id": 1, "name": "laptop"}
    assert client.get("/items").get_json() == [{"id": 1, "name": "laptop"}]


@pytest.mark.parametrize("body", [{}, {"name": ""}, {"name": "   "}])
def test_add_item_requires_name(client, body):
    assert client.post("/items", json=body).status_code == 400


def test_metrics_exposes_request_counter(client):
    client.get("/health")
    body = client.get("/metrics").get_data(as_text=True)
    assert "http_requests_total" in body
    assert 'endpoint="/health"' in body
