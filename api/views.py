from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import UserSerializer, UserTripSerializer, TripSerializer
from .models import User, Trip, TripUser

@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all code users, or create a new user.
    """

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserTripSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
def user_list(request):
    """
    List all code users, or create a new user.
    """

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserTripSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTripSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def trip_list(request):
    """
    List all code trips, or create a new trip.
    """
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])

def trip_detail(request, pk):
    try:
        trip = Trip.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = TripSerializer(trip, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def session_list(request):
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        return Response(
            {'errors': {'title': 'user does not exist'}},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = UserSerializer(user)
    return Response(serializer.data)
