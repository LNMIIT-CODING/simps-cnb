from django.db import models
from django.contrib.postgres.fields import ArrayField


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


class WorkPost(models.Model):
    mobile_num = models.CharField(max_length=10, default="000000000")
    title = models.CharField(max_length=50, default="no title")
    type = ArrayField(models.CharField(max_length=50, default="not available"))
    description = models.TextField(max_length=2000, default="")
    workers_required = models.IntegerField(default=1)
    payment = models.IntegerField(default=1)
    duration = models.IntegerField(default=1)
