from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #Edith has heard about a cool new online to-do app. She goes to check out its home page.
        self.browser.get("http://localhost:8000")

        # She notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        self.fail("Finish the test")

        
        # She is invited to enter a To-Do item straight away.

        # She tpes "Buy peackock feathers" into a test box (Edith's hobby is tying fli-fishing lures)

        # When she hits Enter the page updates and now the page lists "1: Buy peackock feathers" as an item in a To-Do list

        # There is still a text box inviting her to add another item. She enteres "Use peackock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list.

        # Edith wonders, whether the site will remember her list.
        # Then she sees that the site has generated a unique URL for her -- there is some explanatory text to that effect.

        # She visits that URL - her To-Do list is still there.

        # Satisfied, she goes bacl to sleep.

if __name__ == "__main__":
    unittest.main()

