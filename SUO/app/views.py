"""
Definition of views.
"""
# coding: utf8
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest

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
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/statistics.html',
        {
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