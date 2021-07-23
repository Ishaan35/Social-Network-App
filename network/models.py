from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    body = models.CharField(max_length=500, null=False, blank=True, default="")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=True)
    date = models.DateTimeField(default=timezone.now())
    numLikes = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user}, Body: {self.body}, Date: {self.date}, Likes: {self.numLikes}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="liked_post")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_liked")

class Follower(models.Model):
    #user is the person who is following someone
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="isFollowing")
    #following is who the user is following
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="isFollowed")

    
