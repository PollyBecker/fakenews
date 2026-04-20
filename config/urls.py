from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def demo_view(request):
    return render(request, 'demo.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo/', demo_view),
    path('api/auth/', include('apps.users.urls')),
    path('api/workflows/', include('apps.workflows.urls')),
    path('api/sessions/', include('apps.sessions.urls')),
]
