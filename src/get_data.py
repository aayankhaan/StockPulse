from pathlib import Path
import yfinance as yf
import pandas as pd

def download_stock_data(ticker: str, start: str, end: str) -> Path:
    path = Path(f"data/raw/{ticker.lower()}_{start}_{end}.csv")

    if path.exists():
        print(f"data already exists at {path} of the requirment skipping download")
        return path

    print("doawnloading data...")
    data = yf.download(ticker, start=start, end=end)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
        
    data = data.reset_index()

    data.to_csv(path, index=False)
    print(f"done! saved at {path}")
    return path

# placeholder as of now (web input me change karna hai)
if __name__ == "__main__":
    ticker = input("Enter ticker:")
    start = input("Enter start date:")
    end = input("Enter end date:")
    download_stock_data(ticker,start,end)