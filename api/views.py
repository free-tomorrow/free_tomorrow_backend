from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, UserTripSerializer, TripSerializer
from .models import User, Trip

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def detail(self, request, user_id):
        import ipdb; ipdb.set_trace()
        query = User.objects.get(pk = user_id)
        serializer = UserTripSerializer(query)
        return Response(serializer.data)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserTripSerializer(queryset, many=True)
        return Response(serializer.data)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
