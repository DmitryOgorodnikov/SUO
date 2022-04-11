"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render, render_to_response
from django.http import HttpRequest, HttpResponseRedirect
from .models import Tickets
from django.template import Template, RequestContext
from .forms import UserRegistrationForm
from django.contrib.auth.models import User

from django_tables2 import SingleTableView, MultiTableMixin
from django.views.generic.base import TemplateView

from .tables import TicketsTable, TicketsTableCentral
from django.contrib.auth.models import User, Group
import urllib.parse
import re

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
        if Tickets.objects.all().exists() == False:
            Ticket.id_ticket = 0
        else:
            Ticket.id_ticket = Tickets.objects.latest("id_ticket").id_ticket + 1
        name = request.POST.get('name', None)
        if name == "S":
            if Tickets.objects.filter(name_ticket__iregex=r'О...').exists() == False:
                Ticket.name_ticket = 'О' + '001'
            else:
                r = Tickets.objects.filter(name_ticket__iregex=r'О...').latest("name_ticket").name_ticket
                r = int(r[1:4]) + 1
                Ticket.name_ticket = 'О' + '{:03}'.format(r)
        else:
            if Tickets.objects.filter(name_ticket__iregex=r'П...').exists() == False:
                Ticket.name_ticket = 'П' + '001'
            else:
                r = Tickets.objects.filter(name_ticket__iregex=r'П...').latest("name_ticket").name_ticket
                r = int(r[1:4]) + 1
                Ticket.name_ticket = 'П' + '{:03}'.format(r)
        Ticket.save()
        return HttpResponseRedirect('../kiosk/')


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

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(
                request,
                'app/settings.html',
                 {
                 'title':'Операторы',
                 'year':datetime.now().year,
                 }
    )
    else:
        user_form = UserRegistrationForm()
    return render(request, 'app/register.html', {'user_form': user_form, 'year':datetime.now().year,})

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