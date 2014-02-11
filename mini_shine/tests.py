from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
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
        self.response = register(HttpRequest)

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

