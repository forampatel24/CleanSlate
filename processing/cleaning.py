import pandas as pd
import numpy as np


def remove_duplicates(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    subset = kwargs.get('subset', None)
    keep = kwargs.get('keep', 'first')
    return df.drop_duplicates(subset=subset, keep=keep).reset_index(drop=True)


def fill_missing(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    strategy = kwargs.get('strategy', 'constant')
    columns = kwargs.get('columns', None)
    column = kwargs.get('column', None)
    value = kwargs.get('value', '')

    if columns is None and column is not None:
        columns = [column]

    df_copy = df.copy()

    if columns:
        target_cols = [c for c in columns if c in df_copy.columns]
    else:
        target_cols = list(df_copy.columns)

    if strategy == 'constant':
        for col in target_cols:
            df_copy[col] = df_copy[col].fillna(value)

    elif strategy == 'mean':
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].mean())

    elif strategy == 'median':
        for col in target_cols:
            if pd.api.types.is_numeric_dtype(df_copy[col]):
                df_copy[col] = df_copy[col].fillna(df_copy[col].median())

    elif strategy == 'mode':
        for col in target_cols:
            mode_vals = df_copy[col].mode()
            if not mode_vals.empty:
                df_copy[col] = df_copy[col].fillna(mode_vals[0])

    elif strategy == 'remove':
        df_copy = df_copy.dropna(subset=target_cols).reset_index(drop=True)

    return df_copy


def trim_spaces(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    columns = kwargs.get('columns', None)
    df_copy = df.copy()

    target_cols = columns if columns else list(df_copy.columns)

    for col in target_cols:
        if col in df_copy.columns and df_copy[col].dtype == 'object':
            df_copy[col] = df_copy[col].astype(str).str.strip()

    return df_copy


def normalize_text(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    columns = kwargs.get('columns', None)
    df_copy = df.copy()

    target_cols = columns if columns else list(df_copy.columns)

    for col in target_cols:
        if col in df_copy.columns and df_copy[col].dtype == 'object':
            df_copy[col] = df_copy[col].astype(str).str.replace(r'\s+', ' ', regex=True)

    return df_copy


def standardize_capitalization(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    columns = kwargs.get('columns', None)
    style = kwargs.get('style', 'title')

    df_copy = df.copy()
    target_cols = columns if columns else list(df_copy.columns)

    for col in target_cols:
        if col in df_copy.columns and df_copy[col].dtype == 'object':
            if style == 'upper':
                df_copy[col] = df_copy[col].astype(str).str.upper()
            elif style == 'lower':
                df_copy[col] = df_copy[col].astype(str).str.lower()
            elif style == 'title':
                df_copy[col] = df_copy[col].astype(str).str.title()

    return df_copy


def rename_columns(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    mapping = kwargs.get('mapping', {})
    column = kwargs.get('column', None)
    new_name = kwargs.get('new_name', None)
    if column and new_name:
        mapping[column] = new_name
    if not mapping:
        return df
    return df.rename(columns=mapping)
