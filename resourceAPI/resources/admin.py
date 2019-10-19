from django.contrib import admin
from .models import Resource, UserResourceInfo

# Register your models here.
admin.site.register(Resource)
admin.site.register(UserResourceInfo)