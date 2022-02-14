from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, UserTripSerializer, TripSerializer
from .models import User, Trip, TripUser

def unique_trips(data):
    trips = data['trip_set']
    data['trip_set'] = []

    for trip in trips:
        if trip not in data['trip_set']:
            data['trip_set'].append(trip)

    return data

def unique_users(data):
    users = data['users']
    data['users'] = []

    for user in users:
        if user not in data['users']:
            data['users'].append(user)

    return data

@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all code users, or create a new user.
    """

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserTripSerializer(users, many=True)
        users = []
        for user in serializer.data:
            users.append(unique_trips(user))
        return Response(users)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': {'title': 'user could not be created'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'errors': {'title': 'user could not be found'}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTripSerializer(user)
        response_data = serializer.data

        i = 0
        for trip in user.trip_set.all():
            response_data['trip_set'][i]['possible_dates'] = trip.possible_dates()
            i += 1
        return Response(unique_trips(response_data))

@api_view(['GET', 'POST'])
def trip_list(request):
    """ List all trips, or create a new trip. """

    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        trips = []
        for trip in serializer.data:
            trips.append(unique_users(trip))
        return Response(trips)

    elif request.method == 'POST':
        serializer = TripSerializer(data=request.data['trip_info'])
        if serializer.is_valid():
            user = User.objects.get(email=request.data['trip_info']['created_by'])
            trip = serializer.save()

            for date in request.data['dates']:
                TripUser.objects.create(user=user, trip=trip, start_date = date['start_date'], end_date = date['end_date'])

            response_data = serializer.data

            dates = []
            for date in trip.tripuser_set.all():
                dates.append({'start_date': date.start_date, 'end_date': date.end_date})
            response_data['dates'] = dates

            response_data = unique_users(response_data)

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'errors': {'title': 'trip could not be created'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def trip_detail(request, pk):
    """ Get a single trip, or update an existing trip. """

    try:
        trip = Trip.objects.get(pk=pk)
    except Trip.DoesNotExist:
        return Response({'errors': {'title': 'trip does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        response_data = TripSerializer(trip).data
        response_data['possible_dates'] = trip.possible_dates()
        return Response(unique_users(response_data))

    elif request.method == 'PATCH':
        try:
            serializer = TripSerializer(trip, data=request.data['trip_info'], partial=True)
        except KeyError:
            return Response({'errors': {'title': 'trip could not be updated'}}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()

            try:
                user = User.objects.get(pk=request.data['user_id'])
            except User.DoesNotExist:
                return Response({'errors': {'title': 'user could not be found'}}, status=status.HTTP_404_NOT_FOUND)

            for date in request.data['dates']:
                TripUser.objects.create(user=user, trip=trip, start_date = date['start_date'], end_date = date['end_date'])

            return Response(serializer.data)
        return Response({'errors': {'title': 'trip could not be updated'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def session_list(request):
    """ Create a new session for a user on login. """

    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        return Response({'errors': {'title': 'user does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserTripSerializer(user)
    return Response(unique_trips(serializer.data))
