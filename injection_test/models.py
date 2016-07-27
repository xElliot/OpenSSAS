from django.db import models
from .tools import *
# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)
    page = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.name


class Policy(models.Model):
    task = models.ManyToManyField(Task, related_name='policies', blank=True)
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


# 1-get 2-post
class IObject(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='i_objects')
    i_url = models.CharField(max_length=32)
    i_method = models.IntegerField(default=1)

    def __str__(self):
        return get_home(self.i_url)


class IParameter(models.Model):
    i_object = models.ForeignKey(IObject, on_delete=models.CASCADE, related_name='i_parameters')
    name = models.CharField(max_length=32)
    i_value = models.CharField(max_length=32)

    def __str__(self):
        return self.name


