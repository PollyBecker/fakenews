from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkflowViewSet, WorkflowRunViewSet

router = DefaultRouter()
router.register('runs', WorkflowRunViewSet, basename='workflow-run')
router.register('', WorkflowViewSet, basename='workflow')

urlpatterns = [
    path('', include(router.urls)),
]
