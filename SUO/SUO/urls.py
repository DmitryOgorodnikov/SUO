"""
Definition of urls for SUO.
"""
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import TicketsListCentral, register
from tastypie.api import Api
from SUO.resources import TicketsResource, WindowsResource


v1_api = Api(api_name='v1')
v1_api.register(TicketsResource())
#v1_api.register(WindowsResource())
#tickets_resource = TicketsResource()

urlpatterns = [
    path('api/', include(v1_api.urls), name ='Талоны'),
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('settings/delbutton', views.delbutton, name='delbutton'),
    path('settings/edituser', views.edituser, name='edituser'),
    path('settings/settingstable', views.settingstable, name='settingstable'),
    path('register/', views.register, name='register'),
    path('editer/', views.editer, name='editer'),
    path('settings/window/', views.settingsw, name='settingsw'),
    path('settings/window/settingswtable', views.settingswtable, name='settingswtable'),
    path('settings/window/addwindow', views.addwindow, name='addwindow'),
    path('settings/window/changestatusw', views.changestatusw, name='changestatusw'),
    path('settings/window/changeservicew', views.changeservicew, name='changeservicew'),
    path('settings/window/settingswchange', views.settingswchange, name='settingswchange'),
    path('settings/window/wchange', views.wchange, name='wchange'),
    path('settings/window/servicestable', views.servicestable, name='servicestable'),
    path('settings/ops/', views.settingso, name='settingso'),
    path('settings/ops/wchange', views.wchange, name='wchange'),
    path('settings/ops/servicestable', views.servicestable, name='servicestable'),
    path('kiosk/', views.kiosk, name='kiosk'),
    path('kiosk/kioskbtn', views.kioskbtn, name='kioskbtn'),
    path('kiosk/kbutton', views.kbutton, name='kbutton'),
    path('tickets/', 
         TicketsListCentral.as_view
         (
             template_name='app/tickets.html',
             extra_context=
             {
                'title':'Талоны',
                'year':datetime.now().year,
             }
         ),
         name='tickets'),
    path('statistics/', views.statistics, name='statistics'),
    path('statistics/statisticstable', views.statisticstable, name='statisticstable'),
    path('statisticsw/', views.statisticsw, name='statisticsw'),
    path('statisticsw/statisticstablew', views.statisticstablew, name='statisticstablew'),
    path('statisticsall/', views.statisticsall, name='statisticsall'),
    path('windows/login/', views.windows, name='windows'),
    path('windows/login/windowbutton', views.windowbutton, name='windowbutton'),
    path('windows/operator/', views.operator, name='operator'),
    path('windows/operator/operatorbutton', views.operatorbutton, name='operatorbutton'),
    path('windows/operator/nextbutton', views.nextbutton, name='nextbutton'),
    path('windows/operator/cancelbutton', views.cancelbutton, name='cancelbutton'),
    path('windows/operator/breakbutton', views.breakbutton, name='breakbutton'),
    path('windows/operator/redirectbutton', views.redirectbutton, name='redirectbutton'),
    path('windows/operator/redbutton', views.redbutton, name='redbutton'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             redirect_authenticated_user=True,
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]
