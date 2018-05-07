from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def login_user(request, path):
    """
    Serves login view.
    """
    return render(request, 'accounts/login_user.html')

def register_user(request, path):
    """
    Serves register view
    """
    return render(request, 'accounts/register_user.html')