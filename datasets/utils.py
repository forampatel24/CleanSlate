import os
import pandas as pd
import json
from django.core.files.uploadedfile import UploadedFile


def read_uploaded_file(file: UploadedFile) -> pd.DataFrame:
    ext = os.path.splitext(file.name)[1].lower()

    if ext == '.csv':
        return pd.read_csv(file)
    elif ext == '.xlsx':
        return pd.read_excel(file, engine='openpyxl')
    elif ext == '.json':
        return pd.read_json(file)
    else:
        raise ValueError(f'Unsupported file format: {ext}')


def validate_uploaded_file(file: UploadedFile) -> tuple:
    ext = os.path.splitext(file.name)[1].lower()

    if ext not in ('.csv', '.xlsx', '.json'):
        return False, 'Unsupported file format. Please upload CSV, Excel (.xlsx), or JSON files.'

    if file.size == 0:
        return False, 'File is empty.'

    try:
        df = read_uploaded_file(file)
        file.seek(0)
        if df.empty:
            return False, 'File contains no data.'
        return True, df
    except Exception as e:
        return False, f'Could not read file: {str(e)}'
