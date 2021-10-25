"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Users (models.Model):
    id_user = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin = models.BooleanField(default=False)

class Windows (models.Model):
    id_window = models.IntegerField(primary_key=True)
    id_user = models.ForeignKey(Users,on_delete=models.CASCADE)
    accept = models.BooleanField(default=True)
    receive = models.BooleanField(default=True)

class Tickets (models.Model):
    id_ticket = models.IntegerField(primary_key=True)
    id_window = models.ForeignKey(Windows,on_delete=models.CASCADE)
    name_ticket = models.CharField(max_length=50)
    time_create = models.DateField()
    time_close = models.DateField()