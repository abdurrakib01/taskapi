from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('userinfo/', views.UserInfoView.as_view(), name='getinfo'),
]
