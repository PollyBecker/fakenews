from rest_framework import serializers
from .models import RealtimeSession


class RealtimeSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeSession
        fields = '__all__'
        read_only_fields = ('user', 'started_at', 'last_activity_at')
