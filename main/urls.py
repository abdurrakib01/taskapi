from django.urls import path
from . import views

urlpatterns = [
    path('teams/', views.TeamView.as_view(), name='teams'),
    path('teams/<int:pk>/', views.TaskView.as_view(), name='task'),
]
