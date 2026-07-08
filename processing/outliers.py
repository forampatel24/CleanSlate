import pandas as pd
import numpy as np


def detect_outliers_iqr(df: pd.DataFrame, **kwargs) -> dict:
    columns = kwargs.get('columns', None)
    factor = kwargs.get('factor', 1.5)

    target_cols = columns if columns else [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    results = {}
    df_copy = df.copy()

    for col in target_cols:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - factor * iqr
        upper = q3 + factor * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_indices = outliers.index.tolist()

        results[col] = {
            'q1': float(q1),
            'q3': float(q3),
            'iqr': float(iqr),
            'lower_bound': float(lower),
            'upper_bound': float(upper),
            'outlier_count': len(outliers),
            'outlier_pct': round(len(outliers) / len(df) * 100, 2) if len(df) > 0 else 0,
            'outlier_indices': outlier_indices[:100],
        }

    return results


def detect_outliers_zscore(df: pd.DataFrame, **kwargs) -> dict:
    columns = kwargs.get('columns', None)
    threshold = kwargs.get('threshold', 3)

    target_cols = columns if columns else [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    results = {}

    for col in target_cols:
        if col not in df.columns or not pd.api.types.is_numeric_dtype(df[col]):
            continue

        mean = df[col].mean()
        std = df[col].std()

        if std == 0 or pd.isna(std):
            continue

        z_scores = np.abs((df[col] - mean) / std)
        outliers = df[z_scores > threshold]
        outlier_indices = outliers.index.tolist()

        results[col] = {
            'mean': float(mean),
            'std': float(std),
            'threshold': threshold,
            'outlier_count': len(outliers),
            'outlier_pct': round(len(outliers) / len(df) * 100, 2) if len(df) > 0 else 0,
            'outlier_indices': outlier_indices[:100],
        }

    return results
