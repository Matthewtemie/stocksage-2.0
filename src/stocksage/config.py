"""Central configuration for StockSage.

All constants, paths, and environment-loaded settings live here. Other modules
import from this file instead of redefining values.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env file from project root into os.environ
# Must run before any code below that reads env vars
load_dotenv()

# ═══════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════

# PROJECT_ROOT walks up: config.py -> stocksage/ -> src/ -> repo root
PROJECT_ROOT = Path(__file__).parents[2]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FEATURES_DATA_DIR = DATA_DIR / "features"
MODELS_DIR = PROJECT_ROOT / "models"

# ═══════════════════════════════════════════════════════════════
# STOCKS — what we predict
# ═══════════════════════════════════════════════════════════════

STOCKS: dict[str, str] = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google)",
    "AMZN": "Amazon",
    "NVDA": "NVIDIA",
    "TSLA": "Tesla",
}

# ═══════════════════════════════════════════════════════════════
# DATA RANGE
# ═══════════════════════════════════════════════════════════════

DATA_START = "2022-01-01"  # Earliest date to pull
DATA_END: str | None = None  # None means "up to today"

# ═══════════════════════════════════════════════════════════════
# FEATURES — model input columns
# ═══════════════════════════════════════════════════════════════

FEATURE_COLUMNS: list[str] = [
    "daily_return",
    "price_vs_ma5",
    "price_vs_ma10",
    "price_vs_ma20",
    "volatility_5",
    "volatility_20",
    "daily_range",
    "volume_ratio",
    "return_lag_1",
    "return_lag_2",
    "return_lag_3",
    "return_lag_5",
    "rsi_14",
]

# ═══════════════════════════════════════════════════════════════
# ALPACA API CREDENTIALS (loaded from .env)
# ═══════════════════════════════════════════════════════════════

ALPACA_API_KEY: str | None = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY: str | None = os.getenv("ALPACA_SECRET_KEY")
