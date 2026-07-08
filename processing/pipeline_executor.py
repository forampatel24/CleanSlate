import pandas as pd
import time
from . import cleaning
from . import transformation
from . import validation
from . import conversion
from . import merging
from . import outliers

OPERATION_MAP = {
    'remove_duplicates': cleaning.remove_duplicates,
    'fill_missing': cleaning.fill_missing,
    'trim_spaces': cleaning.trim_spaces,
    'normalize_text': cleaning.normalize_text,
    'standardize_capitalization': cleaning.standardize_capitalization,
    'rename_columns': cleaning.rename_columns,
    'convert_dtype': transformation.convert_dtype,
    'format_dates': transformation.format_dates,
    'uppercase': transformation.uppercase,
    'lowercase': transformation.lowercase,
    'title_case': transformation.title_case,
    'remove_special_chars': transformation.remove_special_chars,
    'add_derived_column': transformation.add_derived_column,
    'validate_emails': validation.validate_email_column,
    'validate_phones': validation.validate_phone_column,
    'validate_dates': validation.validate_date_column,
    'detect_outliers_iqr': outliers.detect_outliers_iqr,
    'detect_outliers_zscore': outliers.detect_outliers_zscore,
    'merge_datasets': merging.merge_datasets,
    'convert_format': conversion.convert_dataframe,
}


def execute_pipeline(df: pd.DataFrame, steps: list, secondary_datasets: dict = None) -> dict:
    start_time = time.time()
    current_df = df.copy()
    summary = []

    for step in steps:
        operation = step.get('operation')
        config = step.get('config', {})

        func = OPERATION_MAP.get(operation)
        if not func:
            summary.append({
                'operation': operation,
                'status': 'skipped',
                'message': f'Unknown operation: {operation}',
            })
            continue

        try:
            if operation in ('merge_datasets',):
                if secondary_datasets and config.get('dataset_key') in secondary_datasets:
                    result = func(current_df, secondary_datasets[config['dataset_key']], **config)
                    current_df = result
                else:
                    summary.append({
                        'operation': operation,
                        'status': 'skipped',
                        'message': 'Secondary dataset not provided',
                    })
                    continue
            elif operation == 'convert_format':
                result, content_type, extension = func(current_df, config.get('target_format', 'csv'))
                summary.append({
                    'operation': operation,
                    'status': 'completed',
                    'message': f'Converted to {config.get("target_format", "csv")}',
                    'output_available': True,
                })
                return {
                    'success': True,
                    'runtime': time.time() - start_time,
                    'summary': summary,
                    'dataframe': current_df,
                    'output': result,
                    'output_content_type': content_type,
                    'output_extension': extension,
                }
            else:
                result = func(current_df, **config)
                current_df = result

            summary.append({
                'operation': operation,
                'status': 'completed',
                'message': f'{step.get("label", operation)} completed',
            })

        except Exception as e:
            summary.append({
                'operation': operation,
                'status': 'error',
                'message': str(e),
            })

    runtime = time.time() - start_time

    return {
        'success': True,
        'runtime': round(runtime, 3),
        'summary': summary,
        'dataframe': current_df,
    }
