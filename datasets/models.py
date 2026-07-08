import os
from django.db import models
from django.conf import settings


class Dataset(models.Model):
    FORMAT_CHOICES = [
        ('csv', 'CSV'),
        ('xlsx', 'Excel'),
        ('json', 'JSON'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='datasets')
    file = models.FileField(upload_to='uploads/')
    original_name = models.CharField(max_length=255)
    file_format = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    file_size = models.BigIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Profiling data cached as JSON
    profiling_data = models.JSONField(null=True, blank=True)
    health_report = models.JSONField(null=True, blank=True)
    health_score = models.FloatField(null=True, blank=True)
    row_count = models.IntegerField(null=True, blank=True)
    column_count = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.original_name

    @property
    def file_extension(self):
        return os.path.splitext(self.original_name)[1].lower()
