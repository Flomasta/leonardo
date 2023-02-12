from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<str:pk>/', views.dashboard, name='dashboard'),
]
