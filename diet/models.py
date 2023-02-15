from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE
# Create your models here.


class Contact(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=11)

