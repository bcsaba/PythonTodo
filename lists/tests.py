from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
from django.http import HttpRequest
import inspect

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        self.assertTrue(hasattr(found.func, "__call__")) # one way to test whether this is a function
        self.assertTrue(inspect.isfunction(found.func))  # another way to test whether this is a function
        self.assertEqual(found.func.__name__, "home_page")

    def test_home_page_returns_correct_url(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b"<!DOCTYPE HTML PUBLIC"))
        self.assertIn(b"<title>To-Do list</title>", response.content)
        self.assertTrue(response.content.strip().endswith(b"</html>"))
