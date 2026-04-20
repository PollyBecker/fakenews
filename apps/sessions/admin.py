from django.contrib import admin
from .models import RealtimeSession


@admin.register(RealtimeSession)
class RealtimeSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'started_at', 'last_activity_at')
    list_filter = ('status',)
