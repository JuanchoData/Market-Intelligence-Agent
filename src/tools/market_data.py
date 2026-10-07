import yfinance as yf


def get_market_data(
    ticker: str,
    period: str = "6mo"
):
    """
    Download historical market data for a stock ticker.

    Example:
    ticker = "NVDA"
    period = "6mo"
    """

    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        raise ValueError(
            f"No market data found for ticker: {ticker}"
        )

    return data