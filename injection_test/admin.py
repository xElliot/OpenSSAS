from django.contrib import admin

# Register your models here.

from .models import Task,Target

admin.site.register(Task)
admin.site.register(Target)