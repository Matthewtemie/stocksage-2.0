"""Alpaca API client and historical bar data fetching.

Pulls OHLCV (Open, High, Low, Close, Volume) data for stocks via the Alpaca
Markets API. Returns clean pandas DataFrames indexed by date.
"""

from datetime import datetime

import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

from stocksage import config


def get_alpaca_client() -> StockHistoricalDataClient | None:
    """Create an authenticated Alpaca client using credentials from config.

    Returns None if credentials are missing.
    """
    if not config.ALPACA_API_KEY or not config.ALPACA_SECRET_KEY:
        print("No Alpaca API keys found in environment.")
        print("Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env")
        return None

    client = StockHistoricalDataClient(
        api_key=config.ALPACA_API_KEY,
        secret_key=config.ALPACA_SECRET_KEY,
    )
    print("Alpaca client authenticated successfully")
    return client


def fetch_stock_data(
    client: StockHistoricalDataClient,
    ticker: str,
    start_date: str = config.DATA_START,
    end_date: str | None = config.DATA_END,
) -> pd.DataFrame | None:
    """Fetch daily OHLCV bars for one ticker from Alpaca.

    Args:
        client: Authenticated Alpaca client from get_alpaca_client().
        ticker: Stock symbol, e.g., "AAPL".
        start_date: Earliest date in "YYYY-MM-DD" format.
        end_date: Latest date in "YYYY-MM-DD" format, or None for today.

    Returns:
        DataFrame with columns [Open, High, Low, Close, Volume] indexed by
        date, or None if the fetch failed.
    """
    print(
        f"Fetching {ticker} from Alpaca "
        f"({start_date} -> {'today' if not end_date else end_date})..."
    )

    try:
        request_params = StockBarsRequest(
            symbol_or_symbols=[ticker],
            timeframe=TimeFrame.Day,
            start=datetime.strptime(start_date, "%Y-%m-%d"),
            end=datetime.strptime(end_date, "%Y-%m-%d") if end_date else None,
        )

        bars = client.get_stock_bars(request_params)
        df = bars.df

        if df.empty:
            print(f"No data returned for {ticker}")
            return None

        # Alpaca returns multi-index (symbol, timestamp) — drop symbol level
        if isinstance(df.index, pd.MultiIndex):
            df = df.loc[ticker]

        # Standardize column names to title case
        df = df.rename(
            columns={
                "open": "Open",
                "high": "High",
                "low": "Low",
                "close": "Close",
                "volume": "Volume",
            }
        )
        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()

        # Clean datetime index — strip timezone, sort, drop NaN rows
        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)
        df = df.dropna().sort_index()

        print(
            f"Got {len(df)} trading days for {ticker} "
            f"({df.index[0].strftime('%Y-%m-%d')} -> "
            f"{df.index[-1].strftime('%Y-%m-%d')})"
        )
        return df

    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
