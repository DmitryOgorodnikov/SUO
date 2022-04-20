"""
Definition of views.
"""
from datetime import datetime
from django.shortcuts import render, render_to_response
from django.views.generic.list import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Tickets, Windows
from django.template import Template, RequestContext
from .forms import UserRegistrationForm, UserChangeForm, WindowsAuthenticationForm
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
        request.session['window_id'] = ''
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

def windowbutton(request):
    if request.GET.get('click', False):
        windows_l = []
        for l in Windows.objects.filter(id = None).values_list('id_window'):
            windows_l.append(l[0])

        return JsonResponse({"windows_l": windows_l}, status=200)


@login_required
def operator(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    window_id = request.session.get('window_id')
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
        if Tickets.objects.filter(time_close = None).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            request.session['ticket'] = ticket

            return JsonResponse({"ticket": ticket}, status=200)

        if request.session.get('Ticket_n') is None:
            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_close = None).earliest('id_ticket')
            Ticket.id_window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, "hour": hour, "minute": minute, "second": second}, status=200)


        else:
            Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
            Ticket.time_close = datetime.now()
            Ticket.status = 'Закрыт'
            Ticket.save()

            if Tickets.objects.filter(time_close = None).exists() == False:
                ticket = 'Текущий талон: Нет талонов в очереди'
                request.session['ticket'] = ticket
                request.session['Ticket_n'] = None
                return JsonResponse({"ticket": ticket}, status=200)

            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_close = None).earliest('id_ticket')
            Ticket.id_window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, "hour": hour, "minute": minute, "second": second}, status=200)


def cancelbutton(request):
    if request.GET.get('click', False):

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Отменен'
        Ticket.save()

        if Tickets.objects.filter(time_close = None).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = None
            return JsonResponse({"ticket": ticket}, status=200)

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(time_close = None).earliest('id_ticket')
        Ticket.id_window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, "hour": hour, "minute": minute, "second": second}, status=200)

def breakbutton(request):
    if request.GET.get('click', False):

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Закрыт'
        Ticket.save()
        ticket = 'Текущий талон: Перерыв'

        time = Ticket.time_close
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, "hour": hour, "minute": minute, "second": second}, status=200)



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

def delbutton(request):
    if request.GET.get('click', False):
        Userdel = (User.objects.filter(id=request.GET.get('idbutton')))[0]
        Userdel.delete()

        return JsonResponse({}, status=200)

def edituser(request):
    if request.GET.get('click', False):
        Useredit = (User.objects.filter(id=request.GET.get('idbutton')))[0]
        request.session['useredit'] = Useredit.id
        return JsonResponse({}, status=200)

def settingstable(request):
    if request.GET.get('click', False):
        user = []
        users = User.objects.exclude(username = 'admin')
        for p in users:
            user.append([p.id, p.username, p.last_name])

        return JsonResponse({"user": user}, status=200)

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

def settingswtable(request):
    if request.GET.get('click', False):
        window = []
        windows = Windows.objects.all()
        for p in windows:
            window.append([p.id_window])

        return JsonResponse({"window": window}, status=200)

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

@login_required
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return HttpResponseRedirect('../settings')
    else:
        user_form = UserRegistrationForm()
        head = 'Создание нового аккаунта'
        subhead = 'Пожалуйста, зарегистрируйте нового пользователя, используя нижеуказанную форму'
        namebutton = 'Создать'
        return render(request, 'app/register.html', {'user_form': user_form,'head': head, 'subhead': subhead, 'namebutton': namebutton, 'year':datetime.now().year,})

def editer(request):
    Useredit = User.objects.filter(id = request.session.get('useredit'))[0]
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=Useredit)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            del request.session['useredit']
            return HttpResponseRedirect('../settings')
    else:
        user_form = UserChangeForm(instance=Useredit)
        head = 'Редактирование аккаунта'
        subhead = 'Пожалуйста, измените данные пользователя, используя нижеуказанную форму'
        namebutton = 'Изменить'
        return render(request, 'app/register.html', {'user_form': user_form,'head': head, 'subhead': subhead, 'namebutton': namebutton, 'year':datetime.now().year,})