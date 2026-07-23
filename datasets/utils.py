import os
import io
import pandas as pd
import json


def read_csv_with_fallback_bytes(raw):
    encodings_to_try = ('utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'cp437', 'mac_roman', 'utf-16')
    for enc in encodings_to_try:
        try:
            decoded = raw.decode(enc)
            return pd.read_csv(io.StringIO(decoded))
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(
        'Could not read CSV file. The file encoding is not supported. '
        'Please save the file as UTF-8 encoded CSV.'
    )


def read_uploaded_file(file) -> pd.DataFrame:
    ext = os.path.splitext(file.name)[1].lower()
    raw = file.read()
    if callable(getattr(file, 'seek', None)):
        try:
            file.seek(0)
        except Exception:
            pass
    if ext == '.csv':
        return read_csv_with_fallback_bytes(raw)
    elif ext == '.xlsx':
        return pd.read_excel(io.BytesIO(raw), engine='openpyxl')
    elif ext == '.json':
        try:
            return pd.read_json(io.BytesIO(raw))
        except ValueError:
            return pd.read_json(raw.decode('utf-8'))
    else:
        raise ValueError(f'Unsupported file format: {ext}')


def validate_uploaded_file(file) -> tuple:
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ('.csv', '.xlsx', '.json'):
        return False, 'Unsupported file format. Please upload CSV, Excel (.xlsx), or JSON files.'

    if file.size == 0:
        return False, 'File is empty.'

    try:
        df = read_uploaded_file(file)
        if callable(getattr(file, 'seek', None)):
            try:
                file.seek(0)
            except Exception:
                pass
        if df.empty:
            return False, 'File contains no data.'
        return True, df
    except Exception as e:
        return False, f'Could not read file: {str(e)}'
