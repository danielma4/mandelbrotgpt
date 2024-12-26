from django.urls import path
from .views import FractalGeneratorView

urlpatterns = [
    path('fractal/', FractalGeneratorView.as_view(), name='fractal'),
]