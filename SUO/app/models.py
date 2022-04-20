"""
Definition of models.
"""

from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import JSONField

class Windows (models.Model):
    id_window = models.IntegerField(primary_key=True, verbose_name="ID Окна")
    id = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True, verbose_name="Окно активно")
    services = JSONField(null=True)

class LogWindows (models.Model):
    id_log = models.IntegerField(primary_key=True)
    id_window = models.ForeignKey(Windows, on_delete=models.PROTECT, verbose_name="ID Окна")
    operator = models.CharField(max_length=50, null=True, verbose_name="Оператор")
    time_login = models.DateTimeField(auto_now_add=True, verbose_name="Время входа")
    time_logout = models.DateTimeField(null=True, verbose_name="Время выхода")

class Tickets (models.Model):
    id_ticket = models.IntegerField(primary_key=True, verbose_name="ID Талона")
    service_p = models.CharField(null=True, max_length=50, verbose_name="Услуга")
    status = models.CharField(null=True, max_length=50, verbose_name="Статус")
    id_window = models.ForeignKey(Windows, null=True, on_delete=models.PROTECT, verbose_name="Окно")
    name_ticket = models.CharField(max_length=50, verbose_name="Талон")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_call = models.DateTimeField(null=True, verbose_name="Время вызова")
    time_pause = models.DurationField(default=timedelta(seconds=0), verbose_name="Время пауз")
    time_close = models.DateTimeField(null=True, verbose_name="Время закрытия")

    def service(self):
        time_service = timedelta(0)
        if self.time_close is not None and self.time_call is not None:
            time_period = self.time_close - self.time_call
            time_service = time_period-self.time_pause
        if time_service == timedelta(seconds=0):
            time_service = None
        return time_service

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    chief = models.BooleanField(default=False, verbose_name="Начальник")


