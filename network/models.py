from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date
from django.core.validators import MaxValueValidator, MinValueValidator


class User(AbstractUser):
    dT = models.DateTimeField(default=datetime.now)

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    content = models.CharField(max_length = 255)
    dTCreated = models.DateTimeField(default=datetime.now)
    dTEdited = models.DateTimeField('date_edited', default=datetime.now)
    Edited = models.BooleanField(default=False)

class Follow(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE, null =True)
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, null =True)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    content = models.CharField(max_length = 100)
    dTCreated = models.DateTimeField(default=datetime.now)
    dTEdited = models.DateTimeField('date_edited', default=datetime.now)
    Edited = models.BooleanField(default=False)

class Reaction(models.Model):
    user = models.ForeignKey(User, related_name='reactor', on_delete=models.CASCADE, null =True)
    post = models.ForeignKey(Post, related_name='posts', on_delete=models.CASCADE, null =True)
    type = models.IntegerField(validators=[MaxValueValidator(9), MinValueValidator(0)],default=0)
