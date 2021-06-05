from django.contrib.auth import get_user_model
from rest_framework import serializers
from tickets.models import Board

User = get_user_model()


class BoardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=255)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        """
        Create and return a new `Board` instance, given the validated data.
        """
        return Board.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Board` instance,
        given the validated data.
        """
        instance.title = validated_data.get('name', instance.name)
        instance.owner = validated_data.get('name', instance.owner)
        instance.save()
        return instance
