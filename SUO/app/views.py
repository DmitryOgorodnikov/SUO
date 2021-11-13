"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from .models import Tickets

from django_tables2 import SingleTableView, MultiTableMixin
from django.views.generic.base import TemplateView

from .tables import TicketsTable, TicketsTableCentral
from django.contrib.auth.models import User, Group 

class TicketsListCentral(MultiTableMixin, TemplateView):
    template_name = 'app/tickets.html'
    tables = [
        TicketsTableCentral(Tickets.objects.exclude(id_window_id = None).filter(time_close = None), exclude=("id_ticket","time_create","time_call","time_pause","time_close", )),
        TicketsTableCentral(Tickets.objects.filter(id_window_id = None), exclude=("id_ticket","id_window_id","time_create","time_call","time_pause","time_close", ))
    ]
    table_pagination = {
        "per_page": 10
    }

class TicketsListView(SingleTableView):
    model = Tickets
    table_class = TicketsTable
    template_name = 'app/statistics.html'

def kiosk(request):
    """Renders the kiosk page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/kiosk.html',
        {
            'title':'Киоск',
        }
    )

def kbutton(request):
    if request.POST.get('click', False):
        Ticket = Tickets()
        Ticket.id_ticket = Tickets.objects.latest("id_ticket").id_ticket + 1
        Ticket.name_ticket = "456"
        Ticket.time_create = datetime.now()
        Ticket.save()
    return HttpResponseRedirect('')

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


def windows(request):
    """Renders the windows page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/windows.html',
        {
            'title':'Окна',
            'year':datetime.now().year,
        }
    )

def operator(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/operator.html',
        {
            'title':'Оператор',
            'year':datetime.now().year,
        }
    )

def settings(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settings.html',
        {
            'title':'Операторы',
            'year':datetime.now().year,
        }
    )

def settingsw(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settingsw.html',
        {
            'title':'Окна',
            'year':datetime.now().year,
        }
    )

def settingso(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settingso.html',
        {
            'title':'ОПС',
            'year':datetime.now().year,
        }
    )