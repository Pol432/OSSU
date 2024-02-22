from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True)
    
class Post(models.Model):
    content = models.TextField()
    date = models.DateField(default=date.today)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)