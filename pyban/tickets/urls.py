from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "tickets"

urlpatterns = [
    path('users', views.users, name='users'),
    path('users/me', views.UserView.as_view(), name='user_current'),
    path('users/<int:user_id>', views.users_get_one, name='user'),
    path('login', views.user_login, name='login'),
    path('boards', views.BoardList.as_view(), name='boards'),
    path('boards/<int:pk>/', views.BoardDetail.as_view(), name='board'),
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
]
