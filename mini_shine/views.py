from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from mini_shine.forms import RegistrationForm

# Create your views here.

def home(request):
    return render_to_response('home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # Create Model here and save it
            return HttpResponseRedirect('/profile/add/personal-details/')
    else:
        form = RegistrationForm()

    return render_to_response('register.html', {'form': form})

