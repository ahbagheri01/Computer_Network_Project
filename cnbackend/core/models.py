from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ADMIN = 1
    MANAGER = 2
    USER = 0
    USER_TYPE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MANAGER, 'manager')
    ]

    full_name=models.CharField(max_length=30)
    type=models.CharField(choices=USER_TYPE_CHOICES, default=USER, max_length=10)
    strike=models.BooleanField(default=False)


class Video(models.Model):
    file=models.FileField(upload_to='videos')
    caption=models.CharField(max_length=50)
    user=models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True)
    banned=models.BooleanField(default=False)


class VideoTag(models.Model):
    label=models.CharField(max_length=15)
    video=models.ForeignKey(to=Video, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['label', 'video'], name='label_video_unique')
        ]


class Like(models.Model):
    video=models.ForeignKey(to=Video, on_delete=models.CASCADE)
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'user'], name='video_user_unique')
        ]


class Comment(models.Model):
    text=models.TextField()
    video=models.ForeignKey(to=Video, on_delete=models.CASCADE)
    user=models.ForeignKey(to=User, on_delete=models.CASCADE)