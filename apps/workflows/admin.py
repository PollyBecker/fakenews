from django.contrib import admin
from .models import Workflow, WorkflowRun


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'trigger_time', 'schedule_type', 'is_active')
    list_filter = ('is_active', 'schedule_type')


@admin.register(WorkflowRun)
class WorkflowRunAdmin(admin.ModelAdmin):
    list_display = ('id', 'workflow', 'status', 'executed_at', 'duration_ms')
    list_filter = ('status',)
    readonly_fields = ('executed_at',)
