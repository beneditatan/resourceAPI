from rest_framework import serializers
from .models import UserResourceInfo, Resource


class UserResourceInfoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = UserResourceInfo
        fields = "__all__"

    def get_user(self, obj):
        return obj.user.username


class ResourceSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = "__all__"

    def get_creator(self, obj):
        return obj.creator.username