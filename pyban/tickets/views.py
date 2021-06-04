from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
import json


def users(request):
    if request.method == 'GET':
        return users_get(request)
    if request.method == 'POST':
        return users_post(request)


def users_get(request):
    users = User.objects.all()
    body = {"users": list(users.values())}
    return JsonResponse(body, status=200)


def users_get_one(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        body = {"id": user.id, "username": user.username}
        return JsonResponse(body, status=200)
    except User.DoesNotExist:
        body = {"message": "User does not exist"}
        return JsonResponse(body, status=404)


def users_post(request):
    try:
        credentials = json.loads(request.body)
        username = credentials['username']
        password = credentials['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        id = user.id
        body = {"id": id, "username": username}
        return JsonResponse(body, status=201)
    except ValueError:
        body = {"message": "Username must be set"}
        return JsonResponse(body, status=400)
    except IntegrityError:
        body = {"message": "User already exists"}
        return JsonResponse(body, status=400)
