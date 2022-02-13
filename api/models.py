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

    def possible_dates(self):
        possible_dates = []
        is_date_valid = True
        is_user_available = False

        id = self.users.first().id

        user_one_trip_users = self.tripuser_set.filter(user_id=id)

        all_users = self.users.all()

        if len(all_users) > 1:
            all_users = list(all_users)
        else:
            all_users = [all_users]

        other_users = []
        for user in all_users:
            if user not in other_users:
                other_users.append(user)

        other_users.pop(0)

        for tripuser in user_one_trip_users:
            narrowed_date_range = {
                'start_date': tripuser.start_date,
                'end_date': tripuser.end_date
            }

            if len(other_users) == 0:
                is_date_valid = True
            else:
                for user in other_users:
                    dates = self.tripuser_set.filter(user_id=user.id)
                    for date in dates:
                        if (date.end_date < narrowed_date_range['end_date'] and date.end_date > narrowed_date_range['start_date']) or (date.start_date > narrowed_date_range['start_date'] and date.start_date < narrowed_date_range['end_date']):
                            if date.start_date > narrowed_date_range['start_date']:
                                narrowed_date_range['start_date'] = date.start_date
                            if date.end_date < narrowed_date_range['end_date']:
                                narrowed_date_range['end_date'] = date.end_date
                            is_user_available = True
                    if is_user_available == False:
                        is_date_valid = False
                    is_user_available = False
            if is_date_valid == True:
                possible_dates.append(narrowed_date_range)
            is_date_valid = True
        return possible_dates

class TripUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    start_date = models.BigIntegerField(default=None)
    end_date = models.BigIntegerField(default=None)
