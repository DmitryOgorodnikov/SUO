"""
Definition of forms.
"""

from django import forms
from django.forms import TextInput,PasswordInput,EmailInput,NullBooleanSelect,SelectMultiple,ModelForm, Select
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.db import models
from .models import Tickets, Windows

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':''}))

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    last_name = forms.CharField(label='ФИО', widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': ''}))

    class Meta:
        model = User
        fields = ('username', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

class WindowsAuthenticationForm(forms.Form):
    id_window = forms.ChoiceField(choices = [('','')], label='Окно')

