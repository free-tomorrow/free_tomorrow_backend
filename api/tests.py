from django.db import IntegrityError
from django.core.exceptions import ValidationError
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
        user_2 = User.objects.create(name='Samuel', email='swd1@gmail.com')

        with self.assertRaises(ValidationError):
            user_2.save()
            user_2.full_clean()
            # This line is required here because Django doesn't run full
            # validation on save. full_clean() manually runs a full validation
