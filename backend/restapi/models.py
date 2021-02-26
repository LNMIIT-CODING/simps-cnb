from django.db import models


class User(models.Model):
    mobile_num = models.CharField(max_length=10)
    location = models.JSONField()
    work_type = models.CharField(max_length=40)
    # first_name = models.CharField(max_length=40)
    # last_name = models.CharField(max_length=40)


class Client(models.Model):
    mobile_num = models.CharField(max_length=10)
    location = models.JSONField()
    # username = models.CharField(max_length=40)
    # password = models.CharField(max_length=250)
    # first_name = models.CharField(max_length=40)
    # last_name = models.CharField(max_length=40)
