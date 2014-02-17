from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from mini_shine.forms import RegistrationForm
from mini_shine.models import Candidate
from django.core.exceptions import ValidationError

# Create your views here.

def home(request):
    return render_to_response('home.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            try:
                id = create_model(cleaned_data)
            except ValidationError:
                raise Exception('Some internal error occured while registration, Please register again')

            return HttpResponseRedirect("/candidate/{id}/add-details/".format(id = id))
    else:
        form = RegistrationForm()

    return render_to_response('register.html', {'form': form})

def create_model(cleaned_data):
    Candidate(
        email = cleaned_data.get('email'),
        first_name = cleaned_data.get('first_name'),
        last_name = cleaned_data.get('last_name'),
        city = cleaned_data.get('city'),
        country = cleaned_data.get('country'),
        gender = cleaned_data.get('gender'),
        password = cleaned_data.get('password'),
        mobile_number = cleaned_data.get('mobile_number')).save()
    return Candidate.objects.get(email = cleaned_data.get('email')).id

def add_details(request):
    pass
