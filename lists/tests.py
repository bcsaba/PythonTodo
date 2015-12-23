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
        generated_content_no_csrfinput = '\n'.join([line if not "csrfmiddlew" in line else "\t  "
                                                    for line in generated_content.split('\n')])
        self.assertEqual(generated_content_no_csrfinput, expected_html)

    # def test_home_page_returns_correct_url_w_test_client(self):
    #     response = self.client.get("/")
    #     self.assertTemplateUsed(response, "home.html")            


        

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
        


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "list.html")
    
    def test_displays_all_items(self):
        Item.objects.create(text = "Itemey 1")
        Item.objects.create(text = "Itemey 2")

        response = self.client.get("/lists/the-only-list-in-the-world/")

        self.assertContains(response, "Itemey 1")
        self.assertContains(response, "Itemey 2")


class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        item_text = "A new list item"
        self.client.post("/lists/new",
                         data = {"item_text": item_text}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new",
                         data = {"item_text": "A new list item"}
        )

        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")
