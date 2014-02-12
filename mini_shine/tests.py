from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from rest_framework.test import APIRequestFactory
from mini_shine.views import home, register
from mini_shine.forms import RegistrationForm


class HomePageTest(TestCase):

    def setUp(self):
        self.response = home(HttpRequest())

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_return_html_response(self):
        self.assertIsInstance(self.response, HttpResponse)

    def test_home_view_renders_a_template(self):
        expected_html = render_to_string('home.html')
        self.assertEqual(self.response.content, expected_html)

    def test_home_page_has_right_title(self):
        self.assertIn('<title>Mini Shine</title>', self.response.content)

    def test_home_page_has_right_header(self):
        self.assertIn('<h1>Mini Shine</h1>', self.response.content)

    def test_home_page_has_register_now_link(self):
        self.assertRegexpMatches(str(self.response.content), r'<a.*>Register Now!</a>')

    def test_register_now_link_has_right_url(self):
        self.assertRegexpMatches(str(self.response.content), r'<a.*?/register/.*?>Register Now!</a>', 'Register Now link doesn\'t have right url')


class RegisterPageTest(TestCase):

    def setUp(self):
        self.response = register(HttpRequest())

    def submit_post_form_to_view(self, link, form_details):
        factory = APIRequestFactory()
        request = factory.post(link, form_details)
        return register(request), RegistrationForm(request.POST)

    def check_registration_validation(self, form_details):
        link = '/register/'
        response, form = self.submit_post_form_to_view(link, form_details)
        expected_html = render_to_string('register.html', {'form': form})
        self.assertEqual(expected_html, response.content)

    def test_register_url_points_to_view(self):
        found = resolve('/register/')
        self.assertEqual(found.func, register)

    def test_register_view_return_http_response(self):
        self.assertIsInstance(self.response, HttpResponse)

    def test_register_view_uses_right_template(self):
        form = RegistrationForm()
        expected_html = render_to_string('register.html', { 'form': form })
        self.assertEqual(expected_html, self.response.content)

    def test_register_view_has_right_title_and_header(self):
        self.assertIn('<title>Register</title>', self.response.content)
        self.assertIn('<h1>Register</h1>', self.response.content)

    def test_register_view_has_form_tag(self):
        self.assertIn('form', self.response.content)

    def test_register_view_has_correct_form_fields(self):
        input_fields_names = ['email', 'password', 'confirm_password', 'mobile_number']
        for field_name in input_fields_names:
            self.assertIn(field_name, self.response.content)

    def test_register_view_redirects_to_profile_add_after_registration(self):
        link = '/register/'
        form_details = {
                'email': 'hspandher@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit3242',
                'mobile_number': '9347384284',
                'terms_and_conditions': 'checked'
            }
        response, placeholder = self.submit_post_form_to_view(link, form_details)
        self.assertEqual(response.status_code, 302)

    def test_register_view_does_not_redirect_after_error_form_info(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit32423',
                'mobile_number': '9347384284324234243343',
                'terms_and_conditions': 'checked'
            }
        self.check_registration_validation(form_details)

    def test_register_view_does_not_accept_invalid_email(self):
        form_details = {
                'email': 'hspandhe.r@outlook@com',
                'password': 'punit3242',
                'confirm_password': 'punit3242',
                'mobile_number': '9347384284',
                'terms_and_conditions': 'checked'
            }
        self.check_registration_validation(form_details)

    def test_register_view_does_not_accept_mobile_number(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit3242',
                'mobile_number': '934738428432323232',
                'terms_and_conditions': True
            }
        self.check_registration_validation(form_details)

    def test_register_view_does_not_accept_if_terms_not_agreed(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit3242',
                'mobile_number': '9347384284',
                'terms_and_conditions': False
            }
        self.check_registration_validation(form_details)

    def test_register_view_not_accept_if_password_not_match_confirm_password(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'password': 'punit3242',
                'confirm_password': 'punit3243',
                'mobile_number': '9347384232',
                'terms_and_conditions': True
            }
        self.check_registration_validation(form_details)


    def test_register_view_does_not_accept_if_fields_are_missing(self):
        form_details = {
                'email': 'hspandher@outlook.com',
                'mobile_number': '9347384284',
                'terms_and_conditions': False
            }
        self.check_registration_validation(form_details)





