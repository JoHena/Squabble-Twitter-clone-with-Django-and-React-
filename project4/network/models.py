from email.policy import default
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    following = models.ManyToManyField('self', null=True, blank=True)
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'creator')
    username = models.CharField(max_length = 40)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    likes = models.ManyToManyField(User, null=True, blank=True)
    content = models.CharField(max_length = 800)
    
    def __str__(self):
        return f"{self.id}: Post by: {self.user} Content: {self.content}"