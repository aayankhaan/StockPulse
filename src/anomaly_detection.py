from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def detect_anomalies(df: pd.DataFrame, contamination: float = 0.01) -> pd.DataFrame:
    features = StandardScaler().fit_transform(df[["Return", "Volume", "Volatility"]])
    split = int(len(df) * 0.8)
    train_feature = features[:split]
    test_feature = features[split:]

    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(train_feature)
    print(f"trained on {len(train_feature)} days evaluated on {len(features)} days total!!")

    test_predictions = model.predict(test_feature)
    anomaly_rate_test = (test_predictions == -1).mean()
    print(f"anomaly rate on unseen test data: {anomaly_rate_test:.2%}")

    df["Anomaly"] = model.predict(features)
    df["AnomalyLabel"] = np.where(df["Anomaly"] == -1, "Anomaly", "Normal")

    return df

def get_top_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    anomalies = df[df["Anomaly"] == -1].copy()
    anomalies["AbsReturn"] = anomalies["Return"].abs()
    anomalies = anomalies.sort_values("AbsReturn", ascending=False)
    return anomalies


def save_anomalies(df: pd.DataFrame, filename: str) -> Path:
    out_path = Path(f"data/processed/{filename}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved to {out_path}")
    return out_path


if __name__ == "__main__":
    df = pd.read_csv("data/processed/features.csv")
    df = detect_anomalies(df)

    print(df["AnomalyLabel"].value_counts())
    print("--------------------------------------------------------------------")

    top_anomalies = get_top_anomalies(df)
    print(top_anomalies[["Date", "Close", "Return", "Volume", "Volatility", "AbsReturn"]])

    save_processed_path = save_anomalies(df, "anomalies.csv")