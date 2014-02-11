from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from mini_shine.views import home


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




