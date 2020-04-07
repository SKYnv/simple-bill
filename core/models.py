from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from concurrency.fields import IntegerVersionField


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    version = IntegerVersionField()
    email = models.EmailField()
    nickname = models.CharField(max_length=32)
    blocked = models.BooleanField(default=False)
    note = models.TimeField(blank=True)
