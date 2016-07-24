from django.db import models

# Create your models here.


class Task(models.Model):
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Target(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='targets')
    name = models.CharField(max_length=32)
    comment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name