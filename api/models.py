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
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.name