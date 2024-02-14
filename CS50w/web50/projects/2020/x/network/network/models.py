from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    body = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
            return f"{self.author} - {self.date_created}"
    
    def serialize(self):
        return {
            'id': self.id,
            'author': self.author.username,
            'body': self.body,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'date_edited': self.date_edited.strftime('%Y-%m-%d %H:%M:%S'),
            'likes': self.likes.count(),
        }