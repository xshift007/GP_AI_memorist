# agents/urls.py
from django.urls import path
from .views import IniciarTesisAPIView

urlpatterns = [
    # La URL completa será /api/iniciar-tesis/
    path('iniciar-tesis/', IniciarTesisAPIView.as_view(), name='iniciar-tesis'),
]