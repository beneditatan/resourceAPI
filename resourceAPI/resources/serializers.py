from rest_framework import serializers
from .models import UserResourceInfo, Resource


class UserResourceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResourceInfo
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"