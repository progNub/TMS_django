from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        db_table = 'user'

# Create your models here.
