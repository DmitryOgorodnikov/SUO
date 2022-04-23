"""
WSGI config for SUO project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

For more information, visit
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

from django.dispatch import receiver
from django.db.backends.signals import connection_created
import json

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'SUO.settings')



from app.models import Windows, Services

with open('services.json', 'r', encoding='utf-8-sig') as f:
    my_json_obj = json.load(f)
    if Services.objects.all().exists() != False:
        lastserv = Services.objects.latest('id_services').services
    else:
        lastserv = ''
    if lastserv != my_json_obj:
        service = Services (services=my_json_obj)
        service.save()
        ls = service.services
        for s in ls:
            if s['status'] == False:
                ls.remove(s)
        Window = Windows.objects.all()
        for i in Window:
            i.services = ls
            i.save()

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = get_wsgi_application()
