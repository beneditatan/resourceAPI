from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.decorators import admin_only
from users.constants import AUTHORIZATION_HEADER

from .models import Resource, ResourceQuota
from .serializers import ResourceQuotaSerializer, ResourceSerializer

# Create your views here.
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_resources_list(request, username):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # check if user is requesting resources own by them
    token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
    token_owner = Token.objects.get(key=token).user
    user = get_object_or_404(User, username=username)

    if user != token_owner:
        return Response({"details": "Unauthorised Access"}, status=status.HTTP_403_FORBIDDEN)

    resources = Resource.objects.filter(creator=user)
    serializer = ResourceSerializer(resources, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


