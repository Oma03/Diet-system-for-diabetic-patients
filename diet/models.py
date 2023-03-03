from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE

# Create your models here.


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=True)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=11)

    def __str__(self):
        return self.firstname


class DetailsN(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    diabetes_type = models.CharField(max_length=100)
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=50)
    activity_level = models.CharField(max_length=500)
    age = models.IntegerField()
    bmr = models.CharField(max_length=50, null=True)
    daily_calories = models.CharField(max_length=100, null=True)

    # def __str__(self):
    #     return self.user.username + " - DetailsN"
