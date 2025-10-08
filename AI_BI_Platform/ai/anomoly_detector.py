import pandas as pd
import numpy as np

class Anomoly_Detector:
    def detect(self, df: pd.DataFrame):
        anomalies = {}
        for col in df.select_dtypes(include=np.number).columns:
            z_scores = (df[col] - df[col].mean()) / df[col].std()
            outliers = df[z_scores.abs() > 3]
            if not outliers.empty:
                anomalies[col] = len(outliers)
            return anomalies or ['No anomalies detected']

    