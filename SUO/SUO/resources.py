from tastypie.resources import ModelResource, fields, ALL_WITH_RELATIONS, ALL
from app.models import Tickets, Windows
from datetime import datetime

class WindowsResource(ModelResource):
    class Meta:
        queryset = Windows.objects.all()
        resource_name = 'windows'
        fields = ['id_window']


class TicketsResource(ModelResource):
    id_window = fields.ForeignKey(WindowsResource,'id_window', null=True, full=True)
    class Meta:
        queryset = Tickets.objects.filter(time_create__contains = datetime.now().date()).filter(time_close = None)
        resource_name = 'tickets'
