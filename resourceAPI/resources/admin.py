from django.contrib import admin
from .models import Resource, ResourceQuota

# Register your models here.
admin.site.register(Resource)
admin.site.register(ResourceQuota)