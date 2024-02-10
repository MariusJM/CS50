from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class PostContent(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"