from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResourceQuota(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quota = models.IntegerField(default=0)

    def __str__(self):
        return '{} resource quota'.format(self.user)


class Resource(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return '[{0}] created resource on {1}'.format(self.creator, self.creation_date)