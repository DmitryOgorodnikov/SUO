# tables.py
import django_tables2 as tables
from .models import Tickets

class TicketsTable(tables.Table):
    class Meta:
        model = Tickets
        template_name = "django_tables2/bootstrap.html"
        fields = ("id_ticket","name_ticket","time_create","time_close","id_window_id","Время обработки" )


