"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, render_to_response
from django.views.generic.list import ListView
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Tickets, Windows, Services
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
import json
import codecs
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import DetailView

def kiosk(request):
    """Renders the kiosk page."""
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/kiosk.html',
        {
            'title':'Киоск',
            'opsname': opsname,
        }
    )

def kioskbtn(request):
    if request.GET.get('click', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

def kbutton(request):
    if request.POST.get('click', False):
        Ticket = Tickets()
        if Tickets.objects.all().exists() == False:
            Ticket.id_ticket = 0
        else:
            Ticket.id_ticket = Tickets.objects.latest("id_ticket").id_ticket + 1
        t = datetime.now().date()
        name = request.POST.get('name')
        Ticket.service_p = name
        name = name.split()
        if len(name) == 3:
            name = list(name[0])[0] + list(name[1])[0] + list(name[2])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:3] + ' ' + str(f'{x:03}')

        elif len(name) == 2:
            name = list(name[0])[0] + list(name[1])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:2] + ' ' + str(f'{x:03}')

        else:
            name = list(name[0])[0]
            if Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').exists() == False:
                r = name + ' 001'
            else:
                r = Tickets.objects.filter(time_create__contains = t).filter(name_ticket__iregex=r''+ name +'\s...').latest("id_ticket").name_ticket
                x = int(r[-3:]) + 1
                r = r[0:1] + ' ' + str(f'{x:03}')
        Ticket.name_ticket = r
        Ticket.status = 'Выдан'
        Ticket.save()
        return JsonResponse({'ticketname':r}, status=200)

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

def statistics(request):
    """Renders the kiosk page."""
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/statistics.html',
        {
            'title':'Статистика',
            'opsname': opsname,
        }
    )

def statisticstable(request):
    if request.GET.get('click', False):
        t = datetime.now().date()
        listoftickets = []
        tickets = Tickets.objects.filter(time_create__contains = t).order_by('id_ticket')
        for p in tickets:
            tc = p.time_create.time().strftime("%H:%M:%S")

            if p.time_call == None:
                tca = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")

            if p.time_close == None:
                tcl = ''
            else:
                tcl = p.time_close.time().strftime("%H:%M:%S")

            if p.id_window == None:
                iw = ''
            else:
                iw = p.id_window.id_window

            if p.operator == None:
                op = ''
            else:
                op = p.operator

            listoftickets.append([p.name_ticket, p.service_p, p.status, tc, tca, tcl, iw, op])
        return JsonResponse({'listoftickets': listoftickets}, status=200)

    if request.GET.get('click2', False):
        date = request.GET.get('date').split(', ')
        date[1] = str(int(date[1]) + 1)
        date = ("-".join(date))
        date = (datetime.strptime(date, "%Y-%m-%d")).date()
        listoftickets = []
        tickets = Tickets.objects.filter(time_create__contains = date).order_by('id_ticket')
        for p in tickets:
            tc = p.time_create.time().strftime("%H:%M:%S")

            if p.time_call == None:
                tca = ''
            else:
                tca = p.time_call.time().strftime("%H:%M:%S")

            if p.time_close == None:
                tcl = ''
            else:
                tcl = p.time_close.time().strftime("%H:%M:%S")

            if p.id_window == None:
                iw = ''
            else:
                iw = p.id_window.id_window

            if p.operator == None:
                op = ''
            else:
                op = p.operator

            listoftickets.append([p.name_ticket, p.service_p, p.status, tc, tca, tcl, iw, op])
        return JsonResponse({'date': date, 'listoftickets': listoftickets}, status=200)


@login_required
def windows(request):
    if (Windows.objects.filter(id = request.user).exists() != False):
        window = Windows.objects.get(id = request.user)
        window_id = window.id_window
        request.session['window_id'] = window_id
        user = User.objects.get(username=request.user)
        window.id = user
        window.save()
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

def windowbutton(request):
    if request.GET.get('click', False):
        windows_l = []
        for l in Windows.objects.filter(id = None).filter(active = True).values_list('id_window').order_by('id_window'):
            windows_l.append(l[0])

        return JsonResponse({"windows_l": windows_l}, status=200)

    if request.POST.get('click', False):
        window_id = request.POST.get("name")
        request.session['window_id'] = window_id
        window = Windows.objects.get(id_window = window_id)
        user = User.objects.get(username=request.user)
        window.id = user
        window.save()
        return JsonResponse({}, status=200)

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

def operatorbutton(request):
    window_id = request.session.get('window_id')
    if request.GET.get('click', False):
        window = Windows.objects.get(id_window = window_id)
        window.id = None
        window.save()
        request.session['window_id'] = None
        return JsonResponse({}, status=200)

def nextbutton(request):
    t = datetime.now().date()
    #request.session['Ticket_n'] = None
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        if (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = None).filter(service_p__in = services).exists() == False) and (Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = request.session.get('window_id')).filter(service_p__in = services).exists() == False):
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга:'
            request.session['ticket'] = ticket
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)

        elif request.session.get('Ticket_n') is None:
            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = None).filter(service_p__in = services).earliest('id_ticket')
            Ticket.id_window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.status = 'Вызван'
            Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            service = 'Услуга: ' + Ticket.service_p
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)


        else:
            id=request.session.get('Ticket_n')
            Ticket = Tickets.objects.get(id_ticket=request.session.get('Ticket_n'))
            Ticket.time_close = datetime.now()
            Ticket.status = 'Закрыт'
            Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
            Ticket.save()

            if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = None).filter(service_p__in = services).exists() == False:
                ticket = 'Текущий талон: Нет талонов в очереди'
                service = 'Услуга:'
                request.session['ticket'] = ticket
                request.session['Ticket_n'] = None
                return JsonResponse({"ticket": ticket, 'service': service}, status=200)

            window_id = request.session.get('window_id')
            Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(service_p__in = services).filter(id_window = None).filter(service_p__in = services).earliest('id_ticket')
            Ticket.id_window = Windows.objects.get(id_window=window_id)
            Ticket.time_call = datetime.now()
            Ticket.status = 'Вызван'
            Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
            Ticket.save()
            ticket = 'Текущий талон: ' + Ticket.name_ticket
            service = 'Услуга: ' + Ticket.service_p
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = Ticket.id_ticket

            time = Ticket.time_call
            hour = time.hour
            minute = time.minute
            second = time.second

            return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)


def cancelbutton(request):
    t = datetime.now().date()
    if request.POST.get('click', False):
        service = Windows.objects.get(id_window = request.session.get('window_id')).services
        services = []
        for ser in service:
            if ser['status'] == True:
                services.append(ser['rusname'])

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Отменен'
        Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
        Ticket.save()

        if Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = None).filter(service_p__in = services).exists() == False:
            ticket = 'Текущий талон: Нет талонов в очереди'
            service = 'Услуга: '
            request.session['ticket'] = ticket
            request.session['Ticket_n'] = None
            return JsonResponse({"ticket": ticket, 'service': service}, status=200)

        window_id = request.session.get('window_id')
        Ticket = Tickets.objects.filter(time_create__contains = t).filter(time_close = None).filter(id_window = None).filter(service_p__in = services).earliest('id_ticket')
        Ticket.id_window = Windows.objects.get(id_window=window_id)
        Ticket.time_call = datetime.now()
        Ticket.status = 'Вызван'
        Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
        Ticket.save()
        ticket = 'Текущий талон: ' + Ticket.name_ticket
        service = 'Услуга: ' + Ticket.service_p
        request.session['ticket'] = ticket
        request.session['Ticket_n'] = Ticket.id_ticket

        time = Ticket.time_call
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)

def breakbutton(request):
    if request.POST.get('click', False):

        Ticket = (Tickets.objects.filter(id_ticket=request.session.get('Ticket_n')))[0]
        Ticket.time_close = datetime.now()
        Ticket.status = 'Закрыт'
        Ticket.operator = request.user.last_name + ' (' + request.user.username + ')'
        Ticket.save()
        ticket = 'Текущий талон: Перерыв'
        service = 'Услуга: '

        time = Ticket.time_close
        hour = time.hour
        minute = time.minute
        second = time.second

        return JsonResponse({"ticket": ticket, 'service': service, "hour": hour, "minute": minute, "second": second}, status=200)



@login_required
def settings(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settings.html',
        {
            'title':'Операторы',
            'year':datetime.now().year,
            'opsname': opsname,
        }
    )

def delbutton(request):
    if request.POST.get('click', False):
        Userdel = (User.objects.filter(id=request.POST.get('idbutton')))[0]
        Userdel.delete()

        return JsonResponse({}, status=200)

def edituser(request):
    if request.POST.get('click', False):
        Useredit = (User.objects.filter(id=request.POST.get('idbutton')))[0]
        request.session['useredit'] = Useredit.id
        return JsonResponse({}, status=200)

def settingstable(request):
    if request.POST.get('click', False):
        user = []
        users = User.objects.exclude(username = 'admin')
        for p in users:
            user.append([p.id, p.username, p.last_name])

        return JsonResponse({"user": user}, status=200)

@login_required
def settingsw(request):
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settingsw.html',
        {
            'title':'Окна',
            'year':datetime.now().year,
            'opsname':opsname,
        }
    )

def settingswtable(request):
    if request.GET.get('click', False):
        window = []
        windows = Windows.objects.all().order_by("id_window")
        for p in windows:
            window.append([p.id_window, p.active])

        return JsonResponse({"window": window}, status=200)

def addwindow(request):
    if request.POST.get('click', False):
        number = Windows.objects.all().count()
        window = Windows(id_window = number+1, services = Services.objects.latest('id_services').services)
        window.save()
        return JsonResponse({}, status=200)

def changestatusw(request):
    if request.POST.get('click', False):
        window = Windows.objects.get(id_window = request.POST.get('idwindow'))
        if window.active is True:
            window.active = False
        else:
            window.active = True
        window.save()
        return JsonResponse({}, status=200)

def changeservicew(request):
    if request.POST.get('click', False):
        assert isinstance(request, HttpRequest)
        idwindow = request.POST.get('idwindow')
        request.session['idwindow'] = idwindow
        return JsonResponse({}, status=200)

def settingswchange(request):
    if request.POST.get('click', False):
        idwindow = request.session.get('idwindow')
    else:
        idwindow = request.session.get('idwindow')
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/settingswchange.html',
            {
                'title':'Услуги окна',
                'year':datetime.now().year,
                'idwindow':idwindow,
            }
        )

def servicestable(request):
    if request.GET.get('click', False):
        idwindow = request.session.get('idwindow')
        serviceslist = Windows.objects.get(id_window = idwindow).services
        return JsonResponse({'serviceslist':serviceslist}, status=200)
    if request.GET.get('click2', False):
        serviceslist = Services.objects.latest('id_services').services
        return JsonResponse({'serviceslist':serviceslist}, status=200)

def wchange(request):
    if request.GET.get('click', False):
        listofcheck = request.GET.get('listofcheck')
        listofcheck = listofcheck.split()
        window = Windows.objects.get(id_window = request.session.get('idwindow'))
        i = 0
        for p in listofcheck:
            window.services[i]['status'] = (p == 'true')
            i += 1
        window.save()
        return JsonResponse({}, status=200)

    if request.POST.get('click2', False):
        listofcheck = request.POST.get('listofcheck')
        listofcheck = listofcheck.split()
        service = Services.objects.latest('id_services')
        i = 0
        for p in listofcheck:
            service.services[i]['status'] = (p == 'true')
            i += 1
        listofservices = json.dumps(service.services, ensure_ascii=False)
        with codecs.open("services.json", "w", "utf-8-sig") as temp:
            temp.write(listofservices)
            temp.close()
        service.save()
        ls = service.services
        for s in ls:
            if s['status'] == False:
                ls.remove(s)
        Window = Windows.objects.all()
        for i in Window:
            if len(i.services) != len(ls):
                i.services = ls
                i.save()
        return JsonResponse({}, status=200)

@login_required
def settingso(request):
    """Renders the operator page."""
    assert isinstance(request, HttpRequest)
    with open('config.json', 'r', encoding='utf-8-sig') as f:
        my_json_obj = json.load(f)
        opsname = my_json_obj[0]['name']
    return render(
        request,
        'app/settingso.html',
        {
            'title':'ОПС',
            'year':datetime.now().year,
            'opsname':opsname,
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


class TicketsListCentral(MultiTableMixin, TemplateView):
    template_name = 'app/tickets.html'
    tables = [
        TicketsTableCentral(Tickets.objects.exclude(id_window_id = None).filter(time_close = None), exclude=("id_ticket","time_create","time_call","time_pause","time_close", )),
        TicketsTableCentral(Tickets.objects.filter(id_window_id = None), exclude=("id_ticket","id_window_id","time_create","time_call","time_pause","time_close", ))
    ]
    table_pagination = {
        "per_page": 10
    }