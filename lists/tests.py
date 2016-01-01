from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List
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
        generated_content_no_csrfinput = '\n'.join([line if not "csrfmiddlew" in line else "\t\t\t  "
                                                    for line in generated_content.split('\n')])
        self.assertEqual(generated_content_no_csrfinput, expected_html)

    # def test_home_page_returns_correct_url_w_test_client(self):
    #     response = self.client.get("/")
    #     self.assertTemplateUsed(response, "home.html")            


        

class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()
        
        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first (ever) list item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "Item the second")
        self.assertEqual(second_saved_item.list, list_)
        


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get("/lists/%d/" % (list_.id))
        self.assertTemplateUsed(response, "list.html")
    
    def test_displays_all_items(self):
        print("test_displays_all_items")
        correct_list = List.objects.create()
        Item.objects.create(text = "Itemey 1", list = correct_list)
        Item.objects.create(text = "Itemey 2", list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = "other list item 1", list = other_list)
        Item.objects.create(text = "other list item 2", list = other_list)
        

        response = self.client.get("/lists/%d/" % (correct_list.id))

        self.assertContains(response, "Itemey 1")
        self.assertContains(response, "Itemey 2")
        self.assertNotContains(response, "other list item 1")
        self.assertNotContains(response, "other list item 2")

    def test_passes_correct_list_to_template(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get("/lists/%d/" % (correct_list.id))
        self.assertEqual(response.context["list"], correct_list)
        self.assertNotEqual(response.context["list"], other_list)

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

        list_ = List.objects.first()

        self.assertRedirects(response, "/lists/%d/" % (list_.id))


class NewItemTest(TestCase):
    def test_can_save_a_POST_item_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        item_text = "A new item for an existing list"
        self.client.post("/lists/%d/add_item" % (correct_list.id),
                         data = {"item_text": item_text})
        self.assertEqual(Item.objects.count(), 1)
        added_item = Item.objects.first()
        self.assertEqual(added_item.text, item_text)
        self.assertEqual(added_item.list, correct_list)
        self.assertNotEqual(added_item.list, other_list)

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        
        item_text = "A new item for an existing list"
        response = self.client.post("/lists/%d/add_item" % (correct_list.id),
                         data = {"item_text": item_text})
        self.assertRedirects(response, "/lists/%d/" % (correct_list.id))
