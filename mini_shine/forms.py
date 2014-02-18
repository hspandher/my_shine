from django import forms
from mini_shine.models import Candidate
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):

    email = forms.EmailField(max_length = 40, widget = forms.TextInput(attrs = {'placeholder': 'Email' }))

    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password' }), max_length = 20)

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password' }), max_length = 20)

    first_name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'First Name' }), max_length = 30)

    last_name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Last Name' }), max_length = 30)

    city = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'City' }), max_length = 30)

    country = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Country' }), max_length = 30)

    mobile_number = forms.RegexField(regex = r'^\+?\d{9,15}$', widget = forms.TextInput(attrs = {'placeholder': 'Mobile Number' }))

    gender = forms.ChoiceField(widget = forms.RadioSelect, choices = (('M', 'Male'), ('F', 'Female')))

    terms_and_conditions = forms.BooleanField(label = 'I agree to terms and conditions')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Candidate.objects.filter(email = email):
            raise ValidationError('Email already registered')

        return self.cleaned_data['email']

    def clean_terms_and_conditions(self):
        terms_and_conditions = self.cleaned_data.get('terms_and_conditions')
        if not terms_and_conditions:
            raise forms.ValidationError('You must agree to terms and conditions')

        return self.cleaned_data['terms_and_conditions']

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm Password doesn\'t match')

        return self.cleaned_data


class WorkExperienceForm(forms.Form):

    is_experienced = forms.BooleanField(label = 'Do you have work experience')
    years_of_experience = forms.ChoiceField(choices = tuple((value, str(value)) for value in range(0, 71)), widget = forms.Select(attrs = {'class': 'form-control'}))
    months_of_experience = forms.ChoiceField(choices = tuple((value, str(value)) for value in range(0, 12)), widget = forms.Select(attrs = {'class': 'form-control'}))

class QualificationsForm(forms.Form):

    highest_qualification = forms.ChoiceField(choices = (
            ('10', '10th'),
            ('10+2', '10+2'),
            ('Graduation', 'Graduation'),
            ('Post Graduation', 'Post Graduation'),
            ('Diploma/Vocational Courses', 'Diploma/Vocational Courses')
        ), widget = forms.Select(attrs = {'class': 'form-control'}))

    education_specialization = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Specialization' }), max_length = 40)

    institute_name = forms.CharField(widget = forms.TextInput(attrs = {'placeholder': 'Institute Name' }), max_length = 40)
