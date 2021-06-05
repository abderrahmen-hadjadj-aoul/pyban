from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def canView(self, object):
        return object.canBeViewedBy(self)


class Board(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def canBeViewedBy(self, user):
        return self.owner == user
