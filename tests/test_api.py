from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_root():
    """
    Confirm that the API root endpoint is available.
    """

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    """
    Confirm that the health endpoint works.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_market_query():
    """
    Confirm that a market-only question
    is routed to the market branch.
    """

    response = client.post(
        "/query",
        json={
            "question": (
                "What is NVIDIA's recent volatility "
                "and 30-day return?"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["route"] == "market"

    assert "answer" in data

    assert len(data["answer"]) > 0