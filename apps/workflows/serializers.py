from rest_framework import serializers
from .models import Workflow, WorkflowRun


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'
        read_only_fields = ('user', 'created_at')


class WorkflowRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowRun
        fields = '__all__'
        read_only_fields = ('workflow', 'executed_at')
