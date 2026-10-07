from fastapi.testclient import TestClient
from unittest.mock import patch

from src.api.app import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


@patch("src.agent.calculate_market_metrics")
@patch("src.agent.generate_response")
def test_market_query(
    mock_generate_response,
    mock_calculate_market_metrics
):
    """
    Test the market route without calling
    Yahoo Finance or Ollama.
    """

    mock_calculate_market_metrics.return_value = {
        "ticker": "NVDA",
        "latest_price": 240.0,
        "return_30d_pct": 6.2,
        "annualized_volatility_pct": 38.8,
        "moving_average_20d": 225.0,
        "moving_average_50d": 220.0,
        "price_vs_20d_ma": "above",
        "price_vs_50d_ma": "above",
        "maximum_drawdown_pct": -19.0
    }

    mock_generate_response.return_value = (
        "Annualized volatility is 38.8% "
        "and the 30-day return is 6.2%."
    )

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
    assert "38.8%" in data["answer"]
    assert "6.2%" in data["answer"]