from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def canView(self, object):
        return object.canBeViewedBy(self)

    def canEdit(self, object):
        return object.canBeEditedBy(self)


class Board(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def canBeViewedBy(self, user):
        return self.owner == user

    def canBeEditedBy(self, user):
        return self.owner == user


class Column(models.Model):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board,
                              related_name="columns",
                              on_delete=models.CASCADE)

    def canBeViewedBy(self, user):
        return self.board.owner == user

    def canBeEditedBy(self, user):
        return self.board.owner == user


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def canBeViewedBy(self, user):
        return self.column.board.owner == user

    def canBeEditedBy(self, user):
        return self.column.board.owner == user
