from django.db import models


class User(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=250)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    location = models.JSONField()
