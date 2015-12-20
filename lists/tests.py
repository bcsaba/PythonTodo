from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item
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
        expected_html = render_to_string("home.html")
        generated_content = response.content.decode()
        generated_content_no_csrfinput = '\n'.join([line if not "csrfmiddlew" in line else "\t  " for line in generated_content.split('\n')])
        self.assertEqual(generated_content_no_csrfinput, expected_html)

    def test_home_displays_all_list_items(self):
        item1_text = "itemey 1"
        item2_text = "itemey 2"
        Item.objects.create(text = item1_text)
        Item.objects.create(text = item2_text)

        request = HttpRequest()
        response = home_page(request)

        self.assertIn(item1_text, response.content.decode())
        self.assertIn(item2_text, response.content.decode())
        
    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "A new list item"

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "A new list item"

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

        

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()
        
        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(second_saved_item.text, "Item the second")
        
