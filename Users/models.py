from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    height = models.FloatField(null=True)
    weight = models.IntegerField(null=True)
    goal_weight = models.FloatField(null=True)
    goal_time_period = models.IntegerField(null=True)
    job = models.CharField(max_length=255)
    bmi = models.IntegerField(null=True)
    total_calories = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now=True, null=True)
    history = HistoricalRecords()

    def __str__(self):
        return f'Welcome {self.user.username}!'
