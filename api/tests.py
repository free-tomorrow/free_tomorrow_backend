from django.test import TestCase
# TestCase is a subclass of unittest, the default Python testing framework

class URLTests(TestCase):
    def test_root_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
