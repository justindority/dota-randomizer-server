from django.db import models
from django.contrib.auth.models import User

class BannedHeroes(models.Model):

    hero = models.ForeignKey("Hero", on_delete=models.CASCADE)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

class Profile(models.Model):

    name = models.CharField(max_length=155)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    banned = models.ManyToManyField("Hero", through=BannedHeroes)
    