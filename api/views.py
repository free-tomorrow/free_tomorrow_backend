from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, UserTripSerializer, TripSerializer
from .models import User, Trip

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserTripSerializer(queryset, many=True)
        return Response(serializer.data)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def list(self, request):
        queryset = Trip.objects.all()
        serializer = TripSerializer(queryset, many=True)
        return Response(serializer.data)

