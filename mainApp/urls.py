from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from .forms import LoginForm

urlpatterns = [
    path('', views.dashboard),
]