from django.contrib import admin
from .models import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['original_name', 'user', 'file_format', 'file_size', 'row_count', 'uploaded_at']
    list_filter = ['file_format', 'uploaded_at']
    search_fields = ['original_name', 'user__username']
