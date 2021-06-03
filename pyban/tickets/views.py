from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db import IntegrityError

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
        body = {"id": user.id, "username": user.username, "email": user.email}
        return JsonResponse(body, status=200)
    except User.DoesNotExist as e:
        body = {"message": "User does not exist"}
        return JsonResponse(body, status=404)


def users_post(request):
    try:
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        id = user.id
        body = {"id": id, "username": username, "email": email}
        return JsonResponse(body, status=201)
    except ValueError as e:
        body = {"message": "Username must be set"}
        return JsonResponse(body, status=400)
    except IntegrityError as e:
        body = {"message": "User already exists"}
        return JsonResponse(body, status=400)
