"""
Definition of urls for SUO.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import TicketsListView


urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('settings/window/', views.settingsw, name='settingsw'),
    path('settings/ops/', views.settingso, name='settingso'),
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
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Вход',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]
