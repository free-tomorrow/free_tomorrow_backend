from urllib import response
from django.db import IntegrityError
from django.test import TestCase
from api.models import User, Trip
# TestCase is a subclass of unittest, the default Python testing framework

class URLTests(TestCase):
    def test_get_users(self):
        User.objects.create(name='Sam', email='swd1@gmail.com')
        User.objects.create(name='Sam2', email='swd2@gmail.com')

        response = self.client.get('/users/')
        data = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data[0]['email'], 'swd1@gmail.com')
        self.assertEqual(data[0]['name'], 'Sam')

        self.assertEqual(data[1]['email'], 'swd2@gmail.com')
        self.assertEqual(data[1]['name'], 'Sam2')

        self.assertEqual(len(data), 2)

    def test_get_user(self):
        user = User.objects.create(name='Sam', email='swd1@gmail.com')

        response = self.client.get(f'/users/{user.id}/')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['name'], user.name)

    def test_post_users(self):
        params = {'name': 'Sam', 'email': 'swd1@gmail.com'}

        response = self.client.post('/users/', params)
        data = response.data

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['email'], 'swd1@gmail.com')
        self.assertEqual(data['name'], 'Sam')

    def test_put_user(self):
        user = User.objects.create(name='Sam', email='swd1@gmail.com')

        params = {"name": "Greg", "email": "gwhoisj@gmail.com"}

        response = self.client.put(f'/users/{user.id}/', params, 'application/json')
        data = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], 'gwhoisj@gmail.com')
        self.assertEqual(data['name'], 'Greg')

        user = User.objects.get(pk=data['id'])

        self.assertEqual(user.email, 'gwhoisj@gmail.com')
        self.assertEqual(user.name, 'Greg')

    def test_delete_user(self):
        user = User.objects.create(name='Sam', email='swd1@gmail.com')

        response = self.client.delete(f'/users/{user.id}/')

        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/users/{user.id}/')

        self.assertEqual(response.status_code, 404)

    def test_get_trips(self):
        Trip.objects.create(name='Trip1', created_by='user1', budget=1)
        Trip.objects.create(name='Trip2', created_by='user1', budget=2)

        response = self.client.get('/trips/')
        data = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data[0]['name'], 'Trip1')
        self.assertEqual(data[0]['budget'], 1)

        self.assertEqual(data[1]['name'], 'Trip2')
        self.assertEqual(data[1]['budget'], 2)

        self.assertEqual(len(data), 2)

    def test_get_trip(self):
        trip = Trip.objects.create(name='Trip1', created_by='user1', budget=1)

        response = self.client.get(f'/trips/{trip.id}/')
        data = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data['name'], trip.name)
        self.assertEqual(data['budget'], trip.budget)

    def test_post_trips(self):
        user = User.objects.create(name='Sam', email='swd1@gmail.com')

        params = {'name': 'Trip', 'created_by': user.email, 'budget': 1}

        response = self.client.post('/trips/', params, 'application/json')
        data = response.data

        self.assertEqual(response.status_code, 201)

        self.assertEqual(data['name'], 'Trip')
        self.assertEqual(data['created_by'], user.email)
        self.assertEqual(data['budget'], 1)

        trip = Trip.objects.get(pk=data['id'])
        trip_user = trip.users.first()

        self.assertEqual(user, trip_user)

    def test_put_trip(self):
        trip = Trip.objects.create(name='Trip', created_by='user', budget=1)

        params = {'name': 'Trip2', 'created_by': 'user', 'budget': 10}

        response = self.client.put(f'/trips/{trip.id}/', params, 'application/json')
        data = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data['name'], 'Trip2')
        self.assertEqual(data['created_by'], 'user')
        self.assertEqual(data['budget'], 10)

        response = self.client.get(f'/trips/{trip.id}/')
        data = response.data

        self.assertEqual(data['name'], 'Trip2')
        self.assertEqual(data['created_by'], 'user')
        self.assertEqual(data['budget'], 10)

    def test_delete_trip(self):
        trip = Trip.objects.create(name='Trip', created_by='user', budget=1)

        response = self.client.delete(f'/trips/{trip.id}/')

        self.assertEqual(response.status_code, 204)

        response = self.client.get(f'/users/{trip.id}/')

        self.assertEqual(response.status_code, 404)

class ModelTests(TestCase):
    def test_email_uniqueness(self):
        user_1 = User.objects.create(name='Sam', email='swd1@gmail.com')

        # this context block allows us to assert that an exception will be
        # raised from the code inside of it (email is not unique)
        with self.assertRaises(IntegrityError):
            User.objects.create(name='Samuel', email='swd1@gmail.com')
