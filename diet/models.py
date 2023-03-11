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
    pregnant = models.CharField(max_length=10,  null=True)
    activity_level = models.CharField(max_length=500)
    age = models.IntegerField()
    bmr = models.CharField(max_length=50, null=True)
    bmi = models.CharField(max_length=100, null=True)
    daily_calories = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.username


class DCalorie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    carb_grams = models.CharField(max_length=100)
    protein_grams = models.CharField(max_length=100)
    fat_grams = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
