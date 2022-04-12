"""
Definition of urls for SUO.
"""
from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import TicketsListView, TicketsListCentral, register
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
    path('register/',views.register,name='register'),
    path('settings/window/', views.settingsw, name='settingsw'),
    path('settings/ops/', views.settingso, name='settingso'),
    path('kiosk/', views.kiosk, name='kiosk'),
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
    path('statistics/', 
         TicketsListView.as_view
         (
             template_name='app/statistics.html',
             extra_context=
             {
                'title':'Статистика',
                'year':datetime.now().year,
             }
         ),
         name='statistics'),
    path('windows/login/', views.windows, name='windows'),
    path('windows/operator/', views.operator, name='operator'),
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
    path('logout/', LogoutView.as_view(next_page='login/'), name='logout'),
    path('admin/', admin.site.urls),
]
