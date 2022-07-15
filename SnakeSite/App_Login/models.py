from django.db import models
from django.contrib.auth.models import User


class gameUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='game_user')
    profile_pic = models.ImageField(upload_to='profile_pics')
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.user




