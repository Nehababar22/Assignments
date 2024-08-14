from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import user_list, interest_list, handle_interest
from .views import send_interest, view_interests
from . import views as chat_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout-user'),
    path('users/', user_list, name='user-list'),
    path('send-interest/<int:id>/', send_interest, name='send-interest'),
    path('view-interests/', views.view_interests, name='view-interests'),
    path('interests/', interest_list, name='interest-list'),
    path('handle-interest/<int:interest_id>/<str:action>/', chat_views.handle_interest, name='handle-interest'),
    path("", chat_views.chatPage, name="chat-page"),
]