from django.db import models
from django.contrib.auth.models import User

class userModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    def __str__(self):
        return self.user.username