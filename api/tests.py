from django.db import IntegrityError
from django.test import TestCase
from api.models import User, Trip
# TestCase is a subclass of unittest, the default Python testing framework

class URLTests(TestCase):
    def test_root_path(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class ModelTests(TestCase):
    def test_email_uniqueness(self):
        user_1 = User.objects.create(name='Sam', email='swd1@gmail.com')

        # this context block allows us to assert that an exception will be
        # raised from the code inside of it (email is not unique)
        with self.assertRaises(IntegrityError):
            User.objects.create(name='Samuel', email='swd1@gmail.com')
