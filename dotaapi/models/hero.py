from django.db import models
from django.contrib.auth.models import User


class Hero(models.Model):

    name = models.CharField(max_length=155)
    attribute = models.CharField(max_length=155)
    portraiturl = models.CharField(max_length=155)
    iconurl = models.CharField(max_length=155)