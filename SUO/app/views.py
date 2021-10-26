"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .models import Tickets

from django_tables2 import SingleTableView

from .models import Tickets
from .tables import TicketsTable


class TicketsListView(SingleTableView):
    model = Tickets
    table_class = TicketsTable
    template_name = 'app/statistics.html'

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
            'title':'Настройки СУО',
            'year':datetime.now().year,
        }
    )