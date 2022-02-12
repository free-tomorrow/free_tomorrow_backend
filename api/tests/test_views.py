from django.test import TestCase
from django.urls import reverse
from ..models import User, Trip
from ..serializers import UserSerializer, TripSerializer,  UserTripSerializer
from .. import views

class UserRequestTests(TestCase):
    def create_user(self, name, email):
        return User.objects.create(name=name, email=email)

    def test_get_users(self):
        self.create_user('test', 'test@example.com')
        self.create_user('test2', 'test2@example.com')

        users = User.objects.all()
        response = self.client.get(reverse(views.user_list))
        serializer = UserTripSerializer(users, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]['email'], 'test@example.com')
        self.assertEqual(response.data[0]['name'], 'test')
        self.assertEqual(response.data[1]['email'], 'test2@example.com')
        self.assertEqual(response.data[1]['name'], 'test2')
        self.assertEqual(len(response.data), 2)

    def test_get_user_success(self):
        user = self.create_user('test', 'test@example.com')
        response = self.client.get(reverse(views.user_detail, args=[user.id]))
        serializer = UserTripSerializer(user)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['name'], user.name)

    def test_get_user_failure(self):
        response = self.client.get(reverse(views.user_detail, args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'errors': {'title': 'user could not be found'}})

    def test_post_users_success(self):
        params = {'name': 'test', 'email': 'test@example.com'}
        response = self.client.post(reverse(views.user_list), params)
        serializer = UserSerializer(params)

        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['email'], serializer.data['email'])
        self.assertEqual(response.status_code, 201)

        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['name'], 'test')

    def test_post_users_failure(self):
        self.create_user('test', 'test@example.com')
        params = {'name': 'test', 'email': 'test@example.com'}
        response = self.client.post(reverse(views.user_list), params)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'errors': {'title': 'user could not be created'}})

class TripRequestTests(TestCase):
    def create_trip(self, name, created_by, budget):
        return Trip.objects.create(name=name, created_by=created_by, budget=budget)

    def test_get_trips(self):
        self.create_trip('Trip1', 'test@example.com', 1000)
        self.create_trip('Trip2', 'test@example.com', 2000)

        trips = Trip.objects.all()
        response = self.client.get(reverse(views.trip_list))
        serializer = TripSerializer(trips, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data[0]['name'], 'Trip1')
        self.assertEqual(response.data[0]['budget'], 1000)
        self.assertEqual(response.data[0]['created_by'], 'test@example.com')
        self.assertEqual(response.data[1]['name'], 'Trip2')
        self.assertEqual(response.data[1]['budget'], 2000)
        self.assertEqual(response.data[1]['created_by'], 'test@example.com')
        self.assertEqual(len(response.data), 2)

    def test_get_trip_success(self):
        trip = self.create_trip('Trip1', 'test@example.com', 1000)
        response = self.client.get(reverse(views.trip_detail, args=[trip.id]))
        serializer = TripSerializer(trip)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data['name'], trip.name)
        self.assertEqual(response.data['budget'], trip.budget)
        self.assertEqual(response.data['created_by'], 'test@example.com')

    def test_get_trip_failure(self):
        response = self.client.get(reverse(views.trip_detail, args=[999]))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'errors': {'title': 'trip does not exist'}})

    def test_post_trips_success(self):
        user = User.objects.create(name='test', email='test@example.com')
        params = {'trip_info': {'name': 'Trip', 'created_by': user.email, 'budget': 1}, 'start_date': 1, 'end_date': 2, 'budget': 3}
        response = self.client.post(reverse(views.trip_list), params, 'application/json')
        serializer = TripSerializer(params['trip_info'])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['created_by'], serializer.data['created_by'])
        self.assertEqual(response.data['budget'], serializer.data['budget'])
        self.assertEqual(response.data['name'], 'Trip')
        self.assertEqual(response.data['created_by'], user.email)
        self.assertEqual(response.data['budget'], 1)

        trip = Trip.objects.get(pk=response.data['id'])
        trip_user = trip.users.first()

        self.assertEqual(user, trip_user)

    def test_post_trips_failure(self):
        params = {'trip_info': None }
        response = self.client.post(reverse(views.trip_list), params, 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'errors': {'title': 'trip could not be created'}})

    def test_patch_trip_success(self):
        trip = Trip.objects.create(name='Trip', created_by='user', budget=1)
        params = {'name': 'Trip2', 'created_by': 'user', 'budget': 10}
        response = self.client.patch(reverse(views.trip_detail, args=[trip.id]), params, 'application/json')
        serializer = TripSerializer(params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['created_by'], serializer.data['created_by'])
        self.assertEqual(response.data['budget'], serializer.data['budget'])

        self.assertEqual(response.data['name'], 'Trip2')
        self.assertEqual(response.data['created_by'], 'user')
        self.assertEqual(response.data['budget'], 10)

    def test_patch_trip_failure(self):
        trip = Trip.objects.create(name='Trip', created_by='user', budget=1)
        params = {'hacker_stuff': 1, 'created_by': 'user', 'budget': 10}
        response = self.client.patch(reverse(views.trip_detail, args=[trip.id]), params, 'application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'errors': {'title': 'trip could not be updated'}})

class SessionRequestTests(TestCase):
    def test_post_session_success(self):
        user = User.objects.create(name='test', email='test@example.com')
        params = {'email': 'test@example.com'}
        response = self.client.post(reverse(views.session_list), params)
        serializer = UserSerializer(user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], serializer.data['name'])
        self.assertEqual(response.data['email'], serializer.data['email'])
        self.assertEqual(response.data['name'], 'test')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_post_session_wrong_email(self):
        user = User.objects.create(name='test', email='test@example.com')
        params = {'email': 'wrong@example.com'}
        response = self.client.post(reverse(views.session_list), params)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, {'errors': {'title': 'user does not exist'}})
