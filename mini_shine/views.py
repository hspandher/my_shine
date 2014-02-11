from django.http import HttpResponse
from django.shortcuts import render_to_response
from mini_shine.forms import RegistrationForm

# Create your views here.

def home(request):
    return render_to_response('home.html')

def register(request):
    form = RegistrationForm()
    return render_to_response('register.html', { 'form': form })

