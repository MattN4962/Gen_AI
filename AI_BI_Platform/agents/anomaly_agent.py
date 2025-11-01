import pandas as pd

class AnomalyAgent:
    def __init__(self):
        self.name = "AnomalyAgent"

    def run(self, df: pd.DataFrame) -> dict:
        anomalies = {}
        for col in df.select_dtypes(include=["int", "float"]).columns:
            mean = df[col].mean()
            std = df[col].std()
            outliers = df[(df[col] < mean - 3*std) | (df[col] > mean + 3*std)]
            if not outliers.empty:
                anomalies[col] = {
                    "mean": mean,
                    "std":std,
                    "num_outliers": len(outliers),
                    "outlier_sample": outliers.head(5).to_dict(orient="records")
                }
        return anomalies