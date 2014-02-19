from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from mini_shine.forms import RegistrationForm, WorkExperienceForm, QualificationsForm, LoginForm
from mini_shine.models import Candidate, WorkExperience, EducationQualifications
from django.core.exceptions import ValidationError
from django.contrib import auth

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

            return HttpResponseRedirect("/candidate/{id}/add-work-experience/".format(id = id))
    else:
        form = RegistrationForm()

    return render_to_response('register.html', {'form': form})

def add_work_experience(request, id):
    id = verify_id_offset(id)

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            try:
                create_work_experience_model(cleaned_data, id)
            except ValidationError:
                raise Exception('Some internal error occured while adding Experiencing Details, Please fill form again')

            return HttpResponseRedirect("/candidate/{id}/add-qualifications/".format(id = id))
    else:
        form = WorkExperienceForm()

    return render_to_response('work_experience.html', { 'form': form, 'target_url': request.get_full_path() })

def add_qualifications(request, id):
    id = verify_id_offset(id)

    if request.method == 'POST':
        form = QualificationsForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            try:
                create_qualifications_model(cleaned_data, id)
            except ValidationError:
                raise Exception('Some internal error occured while adding Qualifications Details, Please fill form again')

            return HttpResponseRedirect("/candidate/{id}/profile/".format(id = id))
    else:
        form = QualificationsForm()

    return render_to_response('qualifications.html', { 'form': form, 'target_url': request.get_full_path() })

def profile(request, id):
    id = verify_id_offset(id)
    candidate = Candidate.objects.get(id = id)
    qualifications = EducationQualifications.objects.get(candidate = candidate)
    work_experience = WorkExperience.objects.get(candidate = candidate)
    return render_to_response('profile.html', { 'candidate': candidate, 'work_experience': work_experience, 'qualifications': qualifications })

def login(request):
    authentication_error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            email = cleaned_data['email']
            password = cleaned_data['password']

            user = auth.authenticate(email = email, password = password)
            id = user.id
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/candidate/{id}/profile/'.format(id = id))
            else:
                authentication_error = 'Invalid Email and Password combination'
    else:
        form = LoginForm()

    return render_to_response('login.html', { 'form': form, 'authentication_error': authentication_error })

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

def create_work_experience_model(cleaned_data, id):
    return WorkExperience(
        candidate = Candidate.objects.get(id = id),
        is_experienced = cleaned_data.get('is_experienced'),
        years_of_experience = cleaned_data.get('years_of_experience'),
        months_of_experience = cleaned_data.get('months_of_experience')
        ).save()

def create_qualifications_model(cleaned_data, id):
    return EducationQualifications(
        candidate = Candidate.objects.get(id = id),
        highest_qualification = cleaned_data.get('highest_qualification'),
        education_specialization = cleaned_data.get('education_specialization'),
        institute_name = cleaned_data.get('institute_name')
        ).save()

def verify_id_offset(id):
    try:
        id = int(id)
        Candidate.objects.filter(id = id)
        return id
    except:
        raise Http404()
