import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

from anomaly_detection import detect_anomalies

def evaluate_with_synthetic_anomalies(df: pd.DataFrame, contamination: float = 0.05, n_injected: int = 15):
    df_test = df.copy()

    np.random.seed(42)
    injected_indices = np.random.choice(df_test.index, size=n_injected, replace=False)

    df_test.loc[injected_indices, "Return"] = df_test["Return"].mean() + 10 * df_test["Return"].std()

    df_test["true_label"] = 0
    df_test.loc[injected_indices, "true_label"] = 1  

    df_test = detect_anomalies(df_test, contamination=contamination)
    df_test["predicted_label"] = (df_test["Anomaly"] == -1).astype(int)

    precision = precision_score(df_test["true_label"], df_test["predicted_label"])
    recall = recall_score(df_test["true_label"], df_test["predicted_label"])
    f1 = f1_score(df_test["true_label"], df_test["predicted_label"])

    return precision, recall, f1


if __name__ == "__main__":
    df = pd.read_csv("data/processed/features.csv")
    precision, recall, f1 = evaluate_with_synthetic_anomalies(df)

    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-score: {f1:.2f}")