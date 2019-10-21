from django.db import models
from django.contrib.auth.models import User

from .exceptions import QuotaExceededError

# Create your models here.
class UserResourceInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    quota = models.IntegerField(default=0)
    resources_count = models.IntegerField(default=0)

    def __str__(self):
        return '{} resource quota'.format(self.user)


class Resource(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now=True)
    content = models.TextField()

    def __str__(self):
        return '[{0}] created resource on {1}'.format(self.creator, self.creation_date)

    # override django model built-in save function
    def save(self, *args, **kwargs):
        # check if it's an update or creation
        if self.pk is None:         
            # it's a creation
            # check user quota and resource count
            user_resource = UserResourceInfo.objects.get(user=self.creator)
            quota = user_resource.quota
            count = user_resource.resources_count

            if count + 1 <= quota:
                super(Resource, self).save(*args, **kwargs)

                # update user resources count
                user_resource.resources_count += 1
                user_resource.save() 
            else:
                raise QuotaExceededError("You've exceeded your resource quota")
        else:       
            # it's an update
            super(Resource, self).save(*args, **kwargs)

    # override django model built-in delete function
    def delete(self, *args, **kwargs):
        super(Resource, self).delete(*args, **kwargs)
        user_resource = UserResourceInfo.objects.get(user=self.creator)

        # update user resources count
        user_resource.resources_count -= 1
        user_resource.save() 
