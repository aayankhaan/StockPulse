import pandas as pd

def check_feature_correlation(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    corr_matrix = df[features].corr()
    return corr_matrix


if __name__ == "__main__":
    df = pd.read_csv("data/processed/features.csv")
    
    features = ["Return", "Volume", "Volatility"]
    corr_matrix = check_feature_correlation(df, features)
    
    print(corr_matrix)