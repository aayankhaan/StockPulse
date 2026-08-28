import pandas as pd 
from pathlib import Path

def preprocess(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"])

    df = df.set_index("Date")
    df["Return"] = df["Close"].pct_change()
    df["MA_7"] = df["Close"].rolling(7).mean()
    df["MA_20"] = df["Close"].rolling(20).mean()
    df["Volatility"] = df["Return"].rolling(20).std()
    df = df.dropna()

    return df

def save_processed(df: pd.DataFrame, filename: str) -> Path:
    out_path = Path(f"data/processed/{filename}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path)
    print(f"Saved to {out_path}")

    return out_path

if __name__ == "__main__":
    raw_file = input("Raw CSV filename in data/raw/: ")
    df = preprocess(Path(f"data/raw/{raw_file}"))
    save_processed(df, "features.csv")