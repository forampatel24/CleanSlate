from django.db import models
from django.conf import settings


class Pipeline(models.Model):
    OUTPUT_FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pipelines')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    output_format = models.CharField(max_length=10, choices=OUTPUT_FORMAT_CHOICES, default='csv')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class PipelineStep(models.Model):
    OPERATION_CHOICES = [
        ('remove_duplicates', 'Remove Duplicates'),
        ('fill_missing', 'Fill Missing Values'),
        ('trim_spaces', 'Trim Spaces'),
        ('normalize_text', 'Normalize Text'),
        ('standardize_capitalization', 'Standardize Capitalization'),
        ('rename_columns', 'Rename Columns'),
        ('convert_dtype', 'Convert Data Type'),
        ('format_dates', 'Format Dates'),
        ('uppercase', 'Uppercase'),
        ('lowercase', 'Lowercase'),
        ('title_case', 'Title Case'),
        ('remove_special_chars', 'Remove Special Characters'),
        ('add_derived_column', 'Add Derived Column'),
        ('validate_emails', 'Validate Emails'),
        ('validate_phones', 'Validate Phones'),
        ('validate_dates', 'Validate Dates'),
        ('detect_outliers_iqr', 'Detect Outliers (IQR)'),
        ('detect_outliers_zscore', 'Detect Outliers (Z-Score)'),
        ('merge_datasets', 'Merge Datasets'),
    ]

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField()
    operation = models.CharField(max_length=50, choices=OPERATION_CHOICES)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['step_order']
        unique_together = ['pipeline', 'step_order']

    def __str__(self):
        return f'{self.pipeline.name} - Step {self.step_order}: {self.get_operation_display()}'


class ProcessingHistory(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.SET_NULL, null=True, related_name='history')
    dataset = models.ForeignKey('datasets.Dataset', on_delete=models.SET_NULL, null=True, blank=True, related_name='processing_history')
    executed_at = models.DateTimeField(auto_now_add=True)
    runtime = models.FloatField(help_text='Execution time in seconds')
    output_format = models.CharField(max_length=10)
    summary = models.JSONField(default=dict, blank=True, help_text='Summary of operations performed')
    output_file = models.FileField(upload_to='processed/', null=True, blank=True)

    class Meta:
        ordering = ['-executed_at']
        verbose_name_plural = 'processing histories'

    def __str__(self):
        return f'{self.pipeline.name} - {self.executed_at}' if self.pipeline else f'History - {self.executed_at}'
