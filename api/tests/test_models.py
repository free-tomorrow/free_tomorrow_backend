from django.test import TestCase
from api.models import User, Trip, TripUser
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

    def test_trip_possible_dates(self):
        user1= User.objects.create(name='user1', email='user1@example.com')
        user2= User.objects.create(name='user2', email='user2@example.com')
        user3= User.objects.create(name='user3', email='user3@example.com')

        trip = Trip.objects.create(name='trip', created_by='user1@example.com', budget='1')

        TripUser.objects.create(user_id=user1.id, trip_id=trip.id, start_date=1, end_date=10)
        TripUser.objects.create(user_id=user1.id, trip_id=trip.id, start_date=20, end_date=30)

        self.assertEqual(trip.possible_dates(), [
            {
                'start_date': 1,
                'end_date': 10
            },
            {   'start_date': 20,
                'end_date': 30
            }
        ])

        TripUser.objects.create(user_id=user2.id, trip_id=trip.id, start_date=2, end_date=11)
        TripUser.objects.create(user_id=user2.id, trip_id=trip.id, start_date=19, end_date=29)
        TripUser.objects.create(user_id=user2.id, trip_id=trip.id, start_date=40, end_date=50)

        self.assertEqual(trip.possible_dates(), [
            {
                'start_date': 2,
                'end_date': 10
            },
            {   'start_date': 20,
                'end_date': 29
            }
        ])

        TripUser.objects.create(user_id=user3.id, trip_id=trip.id, start_date=100, end_date=101)

        self.assertEqual(trip.possible_dates(), [])