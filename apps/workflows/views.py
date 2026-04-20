from rest_framework import viewsets, permissions
from .models import Workflow, WorkflowRun
from .serializers import WorkflowSerializer, WorkflowRunSerializer


class WorkflowViewSet(viewsets.ModelViewSet):
    serializer_class = WorkflowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Workflow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WorkflowRunViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkflowRunSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkflowRun.objects.filter(workflow__user=self.request.user)
