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


# class Details(models.Model):
#     user = models.OneToOneField(User, on_delete=CASCADE, null=True)
#     diabetes_type = models.Field()
#     weight = models.FloatField()
#     height = models.FloatField()
#     gender = models.Field()
