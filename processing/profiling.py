import pandas as pd
import numpy as np
import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers


def profile_dataset(df: pd.DataFrame) -> dict:
    profile = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'column_names': list(df.columns),
        'columns': {},
    }

    for col in df.columns:
        col_data = df[col]
        dtype = _detect_type(col_data)
        suggested = _suggest_type(col, dtype, col_data)
        nullable = bool(col_data.isnull().any())
        missing_count = int(col_data.isnull().sum())
        missing_pct = round(float(col_data.isnull().mean() * 100), 2)
        unique_count = int(col_data.nunique())

        col_info = {
            'detected_type': dtype,
            'suggested_type': suggested,
            'nullable': nullable,
            'missing_count': missing_count,
            'missing_pct': missing_pct,
            'unique_count': unique_count,
            'sample_values': col_data.dropna().head(5).tolist(),
        }

        if dtype in ('integer', 'float'):
            col_info.update({
                'min': float(col_data.min()) if not col_data.isnull().all() else None,
                'max': float(col_data.max()) if not col_data.isnull().all() else None,
                'mean': float(col_data.mean()) if not col_data.isnull().all() else None,
                'median': float(col_data.median()) if not col_data.isnull().all() else None,
            })

        profile['columns'][col] = col_info

    return profile


def _detect_type(series: pd.Series) -> str:
    dtype = series.dtype
    if pd.api.types.is_integer_dtype(dtype):
        return 'integer'
    if pd.api.types.is_float_dtype(dtype):
        return 'float'
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'datetime'

    sample = series.dropna().astype(str).head(100)
    if sample.empty:
        return 'string'

    if _looks_like_date(sample):
        return 'datetime'
    if _looks_like_numeric(sample):
        return 'float'
    if _looks_like_email(sample):
        return 'email'
    if _looks_like_phone(sample):
        return 'phone'

    return 'string'


def _suggest_type(col_name: str, detected: str, series: pd.Series) -> str:
    name_lower = col_name.lower()
    if any(kw in name_lower for kw in ['email', 'e-mail', 'mail']):
        return 'email'
    if any(kw in name_lower for kw in ['phone', 'mobile', 'contact', 'telephone', 'tel']):
        return 'phone'
    if any(kw in name_lower for kw in ['date', 'time', 'timestamp']):
        return 'datetime'
    if any(kw in name_lower for kw in ['price', 'revenue', 'cost', 'profit', 'amount', 'salary', 'income']):
        return 'currency'
    if any(kw in name_lower for kw in ['id', 'code', 'key', 'number']):
        return detected or 'string'
    if any(kw in name_lower for kw in ['name', 'address', 'city', 'state', 'country', 'description']):
        return 'string'

    return detected or 'string'


def _looks_like_date(sample: pd.Series) -> bool:
    date_patterns = [
        r'\d{4}-\d{2}-\d{2}',
        r'\d{2}/\d{2}/\d{4}',
        r'\d{2}-\d{2}-\d{4}',
        r'\d{4}/\d{2}/\d{2}',
    ]
    match_count = 0
    for val in sample:
        if pd.isna(val):
            continue
        for pat in date_patterns:
            if re.match(pat, str(val)):
                match_count += 1
                break
    return match_count > len(sample) * 0.6


def _looks_like_numeric(sample: pd.Series) -> bool:
    match_count = 0
    for val in sample:
        if pd.isna(val):
            continue
        try:
            float(str(val).replace(',', '').replace('$', '').replace('%', ''))
            match_count += 1
        except (ValueError, TypeError):
            pass
    return match_count > len(sample) * 0.8


def _looks_like_email(sample: pd.Series) -> bool:
    match_count = 0
    for val in sample:
        if pd.isna(val):
            continue
        try:
            validate_email(str(val), check_deliverability=False)
            match_count += 1
        except EmailNotValidError:
            pass
    return match_count > len(sample) * 0.5


def _looks_like_phone(sample: pd.Series) -> bool:
    match_count = 0
    for val in sample:
        if pd.isna(val):
            continue
        try:
            parsed = phonenumbers.parse(str(val), None)
            if phonenumbers.is_valid_number(parsed):
                match_count += 1
        except phonenumbers.NumberParseException:
            pass
    return match_count > len(sample) * 0.5


def generate_health_report(df: pd.DataFrame, profile: dict) -> dict:
    total_rows = len(df)
    total_cells = total_rows * len(df.columns)

    missing_cells = int(df.isnull().sum().sum())
    duplicate_rows = int(df.duplicated().sum())
    missing_pct = round(missing_cells / total_cells * 100, 2) if total_cells else 0

    report = {
        'total_rows': total_rows,
        'total_columns': len(df.columns),
        'missing_cells': missing_cells,
        'missing_pct': missing_pct,
        'duplicate_rows': duplicate_rows,
        'duplicate_pct': round(duplicate_rows / total_rows * 100, 2) if total_rows else 0,
        'columns': {},
    }

    for col in df.columns:
        col_data = df[col]
        col_report = {
            'missing': int(col_data.isnull().sum()),
            'missing_pct': round(float(col_data.isnull().mean() * 100), 2),
            'duplicates_in_column': int(col_data.duplicated().sum()),
        }

        col_type = profile['columns'].get(col, {}).get('detected_type', 'string')

        if col_type == 'email':
            col_report['invalid_emails'] = _count_invalid_emails(col_data)
        elif col_type == 'phone':
            col_report['invalid_phones'] = _count_invalid_phones(col_data)
        elif col_type == 'datetime':
            col_report['invalid_dates'] = _count_invalid_dates(col_data)

        report['columns'][col] = col_report

    return report


def _count_invalid_emails(series: pd.Series) -> int:
    count = 0
    for val in series.dropna():
        try:
            validate_email(str(val), check_deliverability=False)
        except EmailNotValidError:
            count += 1
    return count


def _count_invalid_phones(series: pd.Series) -> int:
    count = 0
    for val in series.dropna():
        try:
            parsed = phonenumbers.parse(str(val), None)
            if not phonenumbers.is_valid_number(parsed):
                count += 1
        except phonenumbers.NumberParseException:
            count += 1
    return count


def _count_invalid_dates(series: pd.Series) -> int:
    count = 0
    for val in series.dropna():
        try:
            pd.to_datetime(val)
        except (ValueError, TypeError):
            count += 1
    return count


def calculate_health_score(report: dict) -> float:
    penalties = 0.0
    if report['total_rows'] > 0:
        penalties += report.get('missing_pct', 0) * 0.5
        penalties += report.get('duplicate_pct', 0) * 0.5

        for col_name, col_report in report.get('columns', {}).items():
            penalties += col_report.get('missing_pct', 0) * 0.3
            penalties += col_report.get('invalid_emails', 0) / max(report['total_rows'], 1) * 100 * 0.7
            penalties += col_report.get('invalid_phones', 0) / max(report['total_rows'], 1) * 100 * 0.7
            penalties += col_report.get('invalid_dates', 0) / max(report['total_rows'], 1) * 100 * 0.5

    score = max(0, min(100, 100 - penalties))
    return round(score, 2)
