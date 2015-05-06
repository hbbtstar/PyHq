from django.shortcuts import render, redirect
from django.forms import *
from django.contrib.auth import authenticate

def main_view(request):
    if request.user.is_authenticated():
        return render(request, 'main.html')
    else:
        return redirect('login')

