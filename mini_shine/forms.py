from django import forms

class RegistrationForm(forms.Form):

    email = forms.EmailField(max_length = 40)
    password = forms.CharField(widget = forms.PasswordInput(), max_length = 20)
    confirm_password = forms.CharField(widget = forms.PasswordInput(), max_length = 20)
    mobile_number = forms.RegexField(regex = r'^\+?\d{9,15}$')
    terms_and_conditions = forms.ChoiceField(widget = forms.RadioSelect(), choices = ((True, 'Yes'),(False, 'No')))
