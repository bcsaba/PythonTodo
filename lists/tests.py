from django.test import TestCase

class SmokeTest(TestCase):
    def test_mad_maths(self):
        self.assertEqual(1+1, 3)
