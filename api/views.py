from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, UserTripSerializer, TripSerializer
from .models import User, Trip, TripUser

@api_view(['GET', 'POST'])
def user_list(request):
    """ List all users, or create a new user. """

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserTripSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': {'title': 'user could not be created'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_detail(request, pk):
    """ Retrieve a single user. """

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'errors': {'title': 'user could not be found'}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTripSerializer(user)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def trip_list(request):
    """ List all trips, or create a new trip. """

    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TripSerializer(data=request.data['trip_info'])
        if serializer.is_valid():
            user = User.objects.get(email=request.data['trip_info']['created_by'])
            trip = serializer.save()
            TripUser.objects.create(user=user, trip=trip, budget=request.data['budget'], start_date = request.data['start_date'], end_date = request.data['end_date'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'errors': {'title': 'trip could not be created'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def trip_detail(request, pk):
    """ Get a single trip, or update an existing trip. """

    try:
        trip = Trip.objects.get(pk=pk)
    except Trip.DoesNotExist:
        return Response({'errors': {'title': 'trip does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'errors': {'title': 'trip could not be updated'}}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def session_list(request):
    """ Create a new session for a user on login. """

    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        return Response({'errors': {'title': 'user does not exist'}}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)
