from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import user_list


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout-user'),
    path('users/', user_list, name='user-list'),
]