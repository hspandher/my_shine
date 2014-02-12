from django import forms

class RegistrationForm(forms.Form):

    email = forms.EmailField(max_length = 40, widget = forms.TextInput(attrs = {'placeholder': 'Email' }))

    password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Password' }), max_length = 20)

    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs = {'placeholder': 'Confirm Password' }), max_length = 20)

    mobile_number = forms.RegexField(regex = r'^\+?\d{9,15}$', widget = forms.TextInput(attrs = {'placeholder': 'Mobile Number' }))

    terms_and_conditions = forms.BooleanField(label = 'I agree to terms and conditions')

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password and Confirm Password doesn\'t match')
