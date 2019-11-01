from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class userModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    def __str__(self):
        return str(self.id)

class journalModel(models.Model):
    userId = models.ForeignKey(userModel, to_field='id', on_delete=models.CASCADE)
    userIdInt = models.IntegerField(default=None, null=True)
    datetime = models.DateTimeField(default=timezone.now)
    journalEntry = models.CharField(max_length=2000, null=False)