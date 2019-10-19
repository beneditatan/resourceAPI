from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResourceQuota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quota = models.IntegerField(default=0)


class Resource(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
    content = models.TextField()