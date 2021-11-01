"""
Definition of models.
"""

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

class Windows (models.Model):
    id_window = models.IntegerField(primary_key=True, verbose_name="ID Окна")
    id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    accept = models.BooleanField(default=True)
    receive = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

class LogWindows (models.Model):
    id_log = models.IntegerField(primary_key=True)
    id_window = models.ForeignKey(Windows, on_delete=models.PROTECT)
    operator = models.CharField(max_length=50, null=True)
    time_login = models.DateTimeField(auto_now_add=True)
    time_logout = models.DateTimeField(null=True)

class Tickets (models.Model):
    id_ticket = models.IntegerField(primary_key=True, verbose_name="ID Талона")
    id_window = models.ForeignKey(Windows, on_delete=models.PROTECT)
    name_ticket = models.CharField(max_length=50)
    time_create = models.DateTimeField(auto_now_add=True)
    time_call = models.DateTimeField(null=True)
    time_pause = models.DurationField(default=timedelta(seconds=0))
    time_close = models.DateTimeField(null=True)

