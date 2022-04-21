"""
Package for the application.
"""
from django.dispatch import receiver
from django.db.backends.signals import connection_created
import json


@receiver(connection_created)
def my_receiver(connection, **kwargs):
    with connection.cursor() as cursor:
            from .models import Windows, Services
            with open('config.json', 'r') as f:
                my_json_obj = json.load(f)
            
            lastserv = Services.objects.latest('id_services').services
            if lastserv != my_json_obj:
                service = Services (services=my_json_obj)
                service.save()
                Window = Windows.objects.all()
                for i in Window:
                    i.services = my_json_obj
                    i.save()