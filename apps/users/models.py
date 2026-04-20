from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    timezone = models.CharField(max_length=50, default='America/Sao_Paulo')
    preferred_voice = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'users'
