"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render, render_to_response
from django.views.generic.list import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Tickets, Windows
from .forms import WindowsAuthenticationForm
from django.template import Template, RequestContext
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django_tables2 import SingleTableView, MultiTableMixin
from django.views.generic.base import TemplateView

from .tables import TicketsTable, TicketsTableCentral
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
import urllib.parse
import re
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import DetailView

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

@login_required
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


@login_required
def windows(request):

    if request.method == "POST":
        window_id = request.POST.get("id_window")
        request.session['window_id'] = window_id
        return HttpResponseRedirect('../operator/')
    else:
        form = WindowsAuthenticationForm()
        return render(
            request,
            'app/windows.html',
            {
                'title':'Окна',
                'year':datetime.now().year,
                'form': form,
            }
    )


@login_required
def operator(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    window_id = request.session.get('window_id')
#    request.session['ticket'] = Tickets.objects.filter(id_window = None)[:1]

#    if request.method == "POST":
#        request.session['ticket'] = Tickets.objects.filter(id_window = None)[:1]
#        return HttpResponse()
#    else:
    return render(
        request,
        'app/operator.html',
        {
            'title':'Оператор',
            'year':datetime.now().year,
            'window_id': window_id,
        }
    )

def nextbutton(request):
    if request.GET.get('click', False):
        window_id = request.session.get('window_id')
        Ticket = list(Tickets.objects.filter(id_window = None )[:1])[0]
        Ticket.id_window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        #Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        request.session['ticket'] = ticket

        return JsonResponse({"ticket": ticket}, status=200)

@login_required
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

@login_required
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

@login_required
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

@login_required
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