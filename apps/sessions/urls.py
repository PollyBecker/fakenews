from django.urls import path
from .views import StartSessionView, SessionCommandView, VoiceCommandView, CloseSessionView

urlpatterns = [
    path('start/', StartSessionView.as_view()),
    path('<int:session_id>/command/', SessionCommandView.as_view()),
    path('<int:session_id>/voice/', VoiceCommandView.as_view()),
    path('<int:session_id>/close/', CloseSessionView.as_view()),
]
