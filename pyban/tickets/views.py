import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from rest_framework import status
from .models import Board, Ticket, Column
from .serializers import BoardSerializer, TicketSerializer, ColumnSerializer

User = get_user_model()


def home(request):
    body = {"message": "Hello world !"}
    return JsonResponse(body)


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
    List all boards, or create a new board.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        boards = Board.objects.filter(owner=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data["owner"] = request.user.id
        if "columns" not in data:
            data["columns"] = []
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


# TICKETS


class TicketList(APIView):
    """
    List all tickets, or create a new tickets.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        boardid = request.query_params.get("boardid")
        print("get tickets for board", boardid)
        board = Board.objects.get(pk=boardid)
        if not request.user.canView(board):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        tickets = Ticket.objects.filter(board=board)
        print("tickets found", tickets)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data
        data["owner"] = request.user.id
        column = Column.objects.get(pk=data["column"])
        board = column.board
        if not request.user.canEdit(board):
            error = {"error": "You don't have access to the board"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        request.data["board"] = board.id
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("ticket created", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketDetail(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
            if request.user.canView(ticket):
                serializer = TicketSerializer(ticket)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            body = {"message": "Ticket does not exist"}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
            data = request.data
            if request.user.canView(ticket):
                if "title" in data:
                    ticket.title = data["title"]
                if "description" in data:
                    ticket.description = request.data["description"]
                ticket.save()
                serializer = TicketSerializer(ticket)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("ERROR", e)
            body = {"message": e}
            return Response(body, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
            if request.user.canView(ticket):
                ticket.delete()
                serializer = TicketSerializer(ticket)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            print("ERROR", e)
            body = {"message": "Ticket does not exist"}
            return Response(body, status=status.HTTP_404_NOT_FOUND)


# COLUMNS


class ColumnList(APIView):
    """
    List all columns, or create a new columns.
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format=None):
        board = Board.objects.get(pk=pk)
        if not request.user.canView(board):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        columns = Column.objects.filter(board=board)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        board = Board.objects.get(pk=pk)
        if not request.user.canEdit(board):
            error = {"error": "You don't have access to the board"}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        request.data["board"] = pk
        serializer = ColumnSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
