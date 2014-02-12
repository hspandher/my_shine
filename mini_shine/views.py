from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from mini_shine.forms import RegistrationForm

# Create your views here.

def home(request):
    return render_to_response('home.html')

# @csrf_protect
def register(request):
    form = RegistrationForm()
    # csrfContext = RequestContext(request)
    return render_to_response('register.html', { 'form': form })

