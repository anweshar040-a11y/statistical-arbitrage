import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import START_DATE, END_DATE, NIFTY_STOCKS
from src.data_loader import download_stock

for stock in NIFTY_STOCKS:
    print(f"Downloading {stock}...")
    download_stock(stock, START_DATE, END_DATE)

print("All stocks downloaded!")