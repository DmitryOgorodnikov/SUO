"""
Package for the application.
"""
from django.dispatch import receiver
from django.db.backends.signals import connection_created
import json


@receiver(connection_created)
def my_receiver(connection, **kwargs):
    with connection.cursor() as cursor:
            from .models import Windows
            with open('config.json', 'r') as f:
                my_json_obj = json.load(f)
            Window = Windows.objects.all()
            for i in Window:
                if i.services != my_json_obj: 
                    i.services = my_json_obj
                    i.save()