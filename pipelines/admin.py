from django.contrib import admin
from .models import Pipeline, PipelineStep, ProcessingHistory


class PipelineStepInline(admin.TabularInline):
    model = PipelineStep
    extra = 0


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'output_format', 'created_at', 'updated_at']
    list_filter = ['output_format', 'created_at']
    search_fields = ['name', 'user__username']
    inlines = [PipelineStepInline]


@admin.register(ProcessingHistory)
class ProcessingHistoryAdmin(admin.ModelAdmin):
    list_display = ['pipeline', 'executed_at', 'runtime', 'output_format']
    list_filter = ['output_format', 'executed_at']
