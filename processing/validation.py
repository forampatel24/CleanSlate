import pandas as pd
from email_validator import validate_email, EmailNotValidError
import phonenumbers


def validate_email_column(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    column = kwargs.get('column', '')
    action = kwargs.get('action', 'flag')

    if column not in df.columns:
        return df

    df_copy = df.copy()
    mask = df_copy[column].apply(_is_valid_email)

    if action == 'remove':
        df_copy = df_copy[mask].reset_index(drop=True)
    else:
        df_copy['_email_valid'] = mask

    return df_copy


def validate_phone_column(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    column = kwargs.get('column', '')
    action = kwargs.get('action', 'flag')
    region = kwargs.get('region', None)

    if column not in df.columns:
        return df

    df_copy = df.copy()
    mask = df_copy[column].apply(lambda x: _is_valid_phone(x, region))

    if action == 'remove':
        df_copy = df_copy[mask].reset_index(drop=True)
    else:
        df_copy['_phone_valid'] = mask

    return df_copy


def validate_date_column(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    column = kwargs.get('column', '')
    action = kwargs.get('action', 'flag')
    date_format = kwargs.get('date_format', None)

    if column not in df.columns:
        return df

    df_copy = df.copy()
    mask = df_copy[column].apply(lambda x: _is_valid_date(x, date_format))

    if action == 'remove':
        df_copy = df_copy[mask].reset_index(drop=True)
    else:
        df_copy['_date_valid'] = mask

    return df_copy


def _is_valid_email(value) -> bool:
    if pd.isna(value):
        return False
    try:
        validate_email(str(value), check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def _is_valid_phone(value, region=None) -> bool:
    if pd.isna(value):
        return False
    try:
        parsed = phonenumbers.parse(str(value), region)
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False


def _is_valid_date(value, date_format=None) -> bool:
    if pd.isna(value):
        return False
    try:
        if date_format:
            pd.to_datetime(value, format=date_format)
        else:
            pd.to_datetime(value)
        return True
    except (ValueError, TypeError):
        return False
