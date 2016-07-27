from django.contrib import admin

# Register your models here.

from .models import Task,Policy

admin.site.register(Task)
admin.site.register(Policy)