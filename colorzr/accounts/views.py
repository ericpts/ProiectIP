from django.http import *
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from .forms import RegisterForm, LoginForm


def login_user(request, path):
    """
    Serves login view.
    """
    form = LoginForm(request.POST or None)
    logout(request)

    if request.POST:
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=raw_password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                print("Error")

    return render(request, 'accounts/login_user.html', {'form': form})


def register_user(request, path):
    """
    Serves register view
    """
    form = RegisterForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    
    return render(request, 'accounts/register_user.html', {'form': form})
