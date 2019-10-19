from rest_framework import serializers
from .models import ResourceQuota, Resource


class ResourceQuotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceQuota
        fields = "__all__"


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"