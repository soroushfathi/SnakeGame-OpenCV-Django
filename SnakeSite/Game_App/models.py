from django.db import models
from django.contrib.auth.models import User


class record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    record = models.BigIntegerField()

    class Meta:
        ordering = ['-record']

    def __str__(self):
        return self.user
