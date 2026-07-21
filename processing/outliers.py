import pandas as pd
import numpy as np


def detect_outliers_iqr(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    columns = kwargs.get('columns', None)
    factor = kwargs.get('factor', 1.5)
    action = kwargs.get('action', 'flag')

    target_cols = columns if columns else [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and not pd.api.types.is_bool_dtype(df[c])]
    df_copy = df.copy()

    outlier_mask = np.zeros(len(df_copy), dtype=bool)

    for col in target_cols:
        if col not in df.columns:
            continue

        col_series = df_copy[col]
        if not pd.api.types.is_numeric_dtype(col_series):
            continue
        if pd.api.types.is_bool_dtype(col_series):
            continue

        col_values = col_series.astype(float).values
        if col_values.size == 0:
            continue

        non_null = col_values[~np.isnan(col_values)]
        if len(non_null) < 4:
            continue

        unique_count = len(np.unique(non_null))
        if unique_count < 3:
            continue

        q1 = np.percentile(non_null, 25)
        q3 = np.percentile(non_null, 75)
        iqr = q3 - q1

        if np.isnan(iqr) or iqr == 0:
            continue

        lower = q1 - factor * iqr
        upper = q3 + factor * iqr

        col_mask = (col_values < lower) | (col_values > upper)
        outlier_mask = np.logical_or(outlier_mask, col_mask)

    if action == 'remove':
        df_copy = df_copy[~outlier_mask].reset_index(drop=True)
    else:
        df_copy['_outlier_iqr'] = outlier_mask

    return df_copy


def detect_outliers_zscore(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    columns = kwargs.get('columns', None)
    threshold = kwargs.get('threshold', 3)
    action = kwargs.get('action', 'flag')

    target_cols = columns if columns else [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and not pd.api.types.is_bool_dtype(df[c])]
    df_copy = df.copy()

    outlier_mask = np.zeros(len(df_copy), dtype=bool)

    for col in target_cols:
        if col not in df.columns:
            continue

        col_series = df_copy[col]
        if not pd.api.types.is_numeric_dtype(col_series):
            continue
        if pd.api.types.is_bool_dtype(col_series):
            continue

        col_values = col_series.astype(float).values
        if col_values.size == 0:
            continue

        non_null = col_values[~np.isnan(col_values)]
        if len(non_null) < 3:
            continue

        mean = np.mean(non_null)
        std = np.std(non_null)

        if std == 0 or np.isnan(std):
            continue

        z_scores = np.abs((col_values - mean) / std)
        col_mask = z_scores > threshold
        outlier_mask = np.logical_or(outlier_mask, col_mask)

    if action == 'remove':
        df_copy = df_copy[~outlier_mask].reset_index(drop=True)
    else:
        df_copy['_outlier_zscore'] = outlier_mask

    return df_copy
