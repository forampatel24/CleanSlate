import pandas as pd
import io


def convert_dataframe(df: pd.DataFrame, target_format: str, **kwargs) -> tuple:
    if target_format == 'csv':
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer.read(), 'text/csv', '.csv'

    elif target_format == 'xlsx':
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        buffer.seek(0)
        return buffer.getvalue(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx'

    elif target_format == 'json':
        orient = kwargs.get('orient', 'records')
        buffer = io.StringIO()
        df.to_json(buffer, orient=orient, date_format='iso')
        buffer.seek(0)
        return buffer.read(), 'application/json', '.json'

    raise ValueError(f'Unsupported target format: {target_format}')
