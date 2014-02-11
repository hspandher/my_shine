from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from mini_shine.views import home


class HomePageTest(TestCase):

    def setup(self):
        self.response = home(HttpRequest())

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_return_html_response(self):
        response = home(HttpRequest())
        self.assertIsInstance(response, HttpResponse)

    def test_home_view_renders_a_template(self):
        response = home(HttpRequest())
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content, expected_html)

    def test_home_page_has_right_title(self):
        response = home(HttpRequest())
        self.assertIn('<title>Mini Shine</title>', response.content)

    def test_home_page_has_right_header(self):
        response = home(HttpRequest())
        self.assertIn('<h1>Mini Shine</h1>', response.content)

    def test_home_page_has_register_now_link(self):
        response = home(HttpRequest())
        self.assertRegexpMatches(str(response.content), r'<a.*>Register Now!</a>')

    def test_register_now_link_has_right_url(self):
        response = home(HttpRequest)

