import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework import status
from .models import Board
from .serializers import BoardSerializer

User = get_user_model()

# LOGIN


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


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        body = {"id": user.id, "username": user.username}
        return Response(body)


# LOGIN


def user_login(request):
    credentials = json.loads(request.body)
    username = credentials['username']
    password = credentials['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        body = {"id": user.id, "username": username}
        return JsonResponse(body, status=200)
    else:
        body = {"message": "Wrong credentials"}
        return JsonResponse(body, status=403)


# BOARD


class BoardList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        boards = Board.objects.filter(owner=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data["owner"] = request.user.id
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        try:
            board = Board.objects.get(pk=pk)
            if request.user.canView(board):
                serializer = BoardSerializer(board)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            body = {"message": "Board does not exist"}
            return Response(body, status=status.HTTP_404_NOT_FOUND)
