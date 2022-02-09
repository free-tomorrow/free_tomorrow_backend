from asyncore import read
from rest_framework import serializers
from .models import User, Trip, TripUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email')

class TripUserSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = TripUser
        fields = ('budget', 'start_date', 'end_date', 'user')

class TripSetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=64)
    created_by = serializers.CharField(max_length=64)
    confirmed = serializers.BooleanField(default=False)
    budget = serializers.IntegerField

class UserTripSerializer(serializers.ModelSerializer):
    trip_set = TripSetSerializer(many = True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'trip_set')

class TripSerializer(serializers.ModelSerializer):
    users = UserSerializer(many = True, read_only = True)
    trip_users = TripUserSerializer(many = True, read_only = True)

    class Meta:
        model = Trip
        fields = ('id', 'name', 'created_by', 'budget', 'confirmed', 'users', 'trip_users')