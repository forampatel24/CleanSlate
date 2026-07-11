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
    'regex_replace': transformation.regex_replace,
    'validate_emails': validation.validate_email_column,
    'validate_phones': validation.validate_phone_column,
    'validate_dates': validation.validate_date_column,
    'detect_outliers_iqr': outliers.detect_outliers_iqr,
    'detect_outliers_zscore': outliers.detect_outliers_zscore,
    'merge_datasets': merging.merge_datasets,
}


def execute_pipeline(df: pd.DataFrame, steps: list, secondary_datasets: dict = None) -> dict:
    start_time = time.time()
    current_df = df.copy()
    summary = []
    converted_output = None
    converted_content_type = None
    converted_extension = None

    for step in steps:
        operation = step.get('operation')
        config = step.get('config', {})

        if operation == 'convert_format':
            target_format = config.get('target_format', 'csv')
            converted_output, converted_content_type, converted_extension = conversion.convert_dataframe(current_df, target_format)
            summary.append({
                'operation': operation,
                'status': 'completed',
                'message': f'Converted to {target_format}',
            })
            continue

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

    result = {
        'success': True,
        'runtime': round(runtime, 3),
        'summary': summary,
        'dataframe': current_df,
    }

    if converted_output is not None:
        result['output'] = converted_output
        result['output_content_type'] = converted_content_type
        result['output_extension'] = converted_extension

    return result
