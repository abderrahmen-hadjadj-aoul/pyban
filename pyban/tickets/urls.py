from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "tickets"

urlpatterns = [
    # USERS
    path('api-token-auth', obtain_auth_token, name='api_token_auth'),
    path('users', views.users, name='users'),
    path('users/me', views.UserView.as_view(), name='user_current'),
    path('users/<int:user_id>', views.users_get_one, name='user'),
    # BOARDS
    path('boards', views.BoardList.as_view(), name='boards'),
    path('boards/<int:pk>', views.BoardDetail.as_view(), name='board'),
    # TICKETS
    path('tickets', views.TicketList.as_view(), name='tickets'),
    path('tickets/<int:pk>', views.TicketDetail.as_view(), name='ticket'),
]
