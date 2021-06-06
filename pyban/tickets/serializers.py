from django.contrib.auth import get_user_model
from rest_framework import serializers
from tickets.models import Board, Ticket, Column

User = get_user_model()


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name', 'owner', 'columns']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'column', 'board']


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'title', 'board']
