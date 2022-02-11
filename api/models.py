from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64, unique= True)

    def __str__(self):
        return self.email

class Trip(models.Model):
    name = models.CharField(max_length=64)
    created_by = models.CharField(max_length=64)
    confirmed = models.BooleanField(default=False)
    budget = models.IntegerField()
    users = models.ManyToManyField(User, through='TripUser')

    def __str__(self):
        return self.name

class TripUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    start_date = models.PositiveIntegerField(default=None)
    end_date = models.PositiveIntegerField(default=None)
