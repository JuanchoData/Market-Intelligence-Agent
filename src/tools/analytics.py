import numpy as np

from src.tools.market_data import get_market_data


def calculate_market_metrics(
    ticker: str,
    period: str = "6mo"
) -> dict:
    """
    Calculate basic market metrics for a stock.

    Metrics:
    - latest price
    - 30-day return
    - annualized volatility
    - 20-day moving average
    - 50-day moving average
    - maximum drawdown
    """

    data = get_market_data(
        ticker=ticker,
        period=period
    )

    close = data["Close"].squeeze()

    daily_returns = close.pct_change().dropna()

    latest_price = float(
        close.iloc[-1]
    )

    if len(close) >= 21:
        return_30d = (
            close.iloc[-1] /
            close.iloc[-21]
            - 1
        )
    else:
        return_30d = np.nan

    annualized_volatility = (
        daily_returns.std()
        * np.sqrt(252)
    )

    moving_average_20d = float(
        close.tail(20).mean()
    )

    moving_average_50d = float(
        close.tail(50).mean()
    )

    rolling_max = close.cummax()

    drawdown = (
        close / rolling_max
        - 1
    )

    maximum_drawdown = float(
        drawdown.min()
    )

    return {
    "ticker": ticker.upper(),

    "latest_price": round(
        latest_price,
        2
    ),

    "return_30d_pct": round(
        float(return_30d) * 100,
        2
    ),

    "annualized_volatility_pct": round(
        float(annualized_volatility) * 100,
        2
    ),

    "moving_average_20d": round(
        moving_average_20d,
        2
    ),

    "moving_average_50d": round(
        moving_average_50d,
        2
    ),

    "price_vs_20d_ma": (
        "above"
        if latest_price > moving_average_20d
        else "below"
    ),

    "price_vs_50d_ma": (
        "above"
        if latest_price > moving_average_50d
        else "below"
    ),

    "maximum_drawdown_pct": round(
        maximum_drawdown * 100,
        2
    )
}