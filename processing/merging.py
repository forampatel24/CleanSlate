import pandas as pd


def merge_datasets(df_left: pd.DataFrame, df_right: pd.DataFrame, **kwargs) -> pd.DataFrame:
    how = kwargs.get('how', 'inner')
    left_on = kwargs.get('left_on', None)
    right_on = kwargs.get('right_on', None)
    left_index = kwargs.get('left_index', False)
    right_index = kwargs.get('right_index', False)

    if left_on and right_on:
        return pd.merge(df_left, df_right, how=how, left_on=left_on, right_on=right_on)
    elif left_index or right_index:
        return pd.merge(df_left, df_right, how=how, left_index=left_index, right_index=right_index)
    else:
        common_cols = list(set(df_left.columns) & set(df_right.columns))
        if common_cols:
            return pd.merge(df_left, df_right, how=how, on=common_cols[0])
        return pd.concat([df_left, df_right], axis=1)
