"""Technical indicator computations.

Each function takes a pandas Series (or two) and returns a pandas Series.
These are pure functions — no DataFrame manipulation, no I/O.
This makes them trivially testable and easy to reuse.
"""

import pandas as pd

# ═══════════════════════════════════════════════════════════════
# MOMENTUM
# ═══════════════════════════════════════════════════════════════


def compute_returns(close: pd.Series) -> pd.Series:
    """Daily percentage return: (close - prev_close) / prev_close.

    Returns NaN for the first row (no previous close to compare against).
    """
    return close.pct_change()


def compute_moving_average(close: pd.Series, window: int) -> pd.Series:
    """Simple moving average of close prices over the given window.

    Returns NaN for the first (window - 1) rows.
    """
    return close.rolling(window).mean()


def compute_price_vs_ma(close: pd.Series, moving_avg: pd.Series) -> pd.Series:
    """How far the current price is above/below its moving average, as a ratio.

    Returns 0.05 when price is 5% above the MA, -0.03 when 3% below, etc.
    """
    return close / moving_avg - 1


# ═══════════════════════════════════════════════════════════════
# VOLATILITY
# ═══════════════════════════════════════════════════════════════


def compute_volatility(returns: pd.Series, window: int) -> pd.Series:
    """Rolling standard deviation of returns — a proxy for volatility.

    Higher values mean the stock has been swinging around more lately.
    """
    return returns.rolling(window).std()


def compute_daily_range(high: pd.Series, low: pd.Series, close: pd.Series) -> pd.Series:
    """Intraday range as a fraction of the closing price.

    Captures how wild the day was, normalized so AAPL ($200) and a $20
    stock are comparable.
    """
    return (high - low) / close


# ═══════════════════════════════════════════════════════════════
# VOLUME
# ═══════════════════════════════════════════════════════════════


def compute_volume_ratio(volume: pd.Series, window: int = 5) -> pd.Series:
    """Today's volume divided by the average over the last `window` days.

    Returns 2.0 if today's volume is double the recent average — often
    a sign of unusual activity.
    """
    volume_ma = volume.rolling(window).mean()
    return volume / volume_ma


# ═══════════════════════════════════════════════════════════════
# LAGGED RETURNS
# ═══════════════════════════════════════════════════════════════


def compute_lagged_return(returns: pd.Series, lag: int) -> pd.Series:
    """The return from `lag` days ago.

    compute_lagged_return(returns, 3) gives you the return from 3 days back,
    aligned to today's row. Useful for capturing short-term momentum.
    """
    return returns.shift(lag)


# ═══════════════════════════════════════════════════════════════
# OSCILLATOR
# ═══════════════════════════════════════════════════════════════


def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    """Relative Strength Index — bounded oscillator between 0 and 100.

    RSI > 70 traditionally signals overbought; RSI < 30 oversold.
    Computed from average gains vs. average losses over the window.
    """
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    return 100 - (100 / (1 + gain / loss))
