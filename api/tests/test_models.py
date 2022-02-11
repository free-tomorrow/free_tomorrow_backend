from django.test import TestCase
from api.models import User, Trip
from django.db.utils import IntegrityError

class UserTests(TestCase):
    def create_user(self, name='test', email='test@example.com'):
        return User.objects.create(name=name, email=email)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), user.email)

    def test_user_attributes(self):
        user = self.create_user()
        self.assertEqual(user.name, 'test')
        self.assertEqual(user.email, 'test@example.com')

    def test_user_email_uniqueness(self):
        user = self.create_user()

        # this context block allows us to assert that an exception will be
        # raised from the code inside of it (email is not unique)
        with self.assertRaises(IntegrityError):
            User.objects.create(name='test', email='test@example.com')

class TripTests(TestCase):
    def create_trip(self, name='Disney', created_by='test@example.com', budget=1000):
        return Trip.objects.create(name=name, created_by=created_by, budget=budget)

    def test_trip_creation(self):
        trip = self.create_trip()
        self.assertTrue(isinstance(trip, Trip))
        self.assertEqual(trip.__str__(), trip.name)

    def test_trip_attributes(self):
        trip = self.create_trip()
        self.assertEqual(trip.name, 'Disney')
        self.assertEqual(trip.created_by, 'test@example.com')
        self.assertEqual(trip.confirmed, False)
        self.assertEqual(trip.budget, 1000)
