from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page
import inspect

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve("/")
        print(found.func)
        self.assertEqual(hasattr(found.func, "__call__"), True) # one way to test whether this is a function
        self.assertEqual(inspect.isfunction(found.func), True)  # another way to test whether this is a function
        self.assertEqual(found.func.__name__, "home_page")
