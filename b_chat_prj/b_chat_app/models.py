from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
#then done creating tables, or chenge
#python manage.py makemigrations <your app name>
#python manage.py migrate

class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    msg = models.CharField(max_length=500, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
