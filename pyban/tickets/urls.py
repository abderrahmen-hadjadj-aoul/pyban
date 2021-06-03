from django.urls import path

from . import views

app_name = "tickets"
urlpatterns = [
    path('users', views.users, name='users'),
    path('users/<int:user_id>', views.users_get_one, name='user'),
]
