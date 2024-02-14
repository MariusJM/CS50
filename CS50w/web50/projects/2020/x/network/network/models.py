from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def following(self, other_user):
        return self.following.filter(following=other_user).exists()
    

class PostContent(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"