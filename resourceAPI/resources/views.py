from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.constants import ADMIN_GROUP, AUTHORIZATION_HEADER
from users.decorators import admin_only
from users.utils import is_member_of

from .exceptions import QuotaExceededError
from .models import Resource, UserResourceInfo
from .serializers import ResourceSerializer, UserResourceInfoSerializer


# Create your views here.
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def get_all_resources(request):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_resources_list(request, username):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # check if user is requesting resources owned by them
    token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
    token_owner = Token.objects.get(key=token).user
    user = get_object_or_404(User, username=username)

    if not is_member_of(token_owner.username, ADMIN_GROUP) and user != token_owner:
        return Response({"details": "Unauthorised Access"}, status=status.HTTP_403_FORBIDDEN)

    resources = Resource.objects.filter(creator=user)
    serializer = ResourceSerializer(resources, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def resource_detail(request, resource_id):
    token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
    token_owner = Token.objects.get(key=token).user

    resource = get_object_or_404(Resource, id=resource_id)

    # check if user is requesting resource owned by them or user is an admin
    if not is_member_of(token_owner.username, ADMIN_GROUP) and resource.creator != token_owner:
        return Response({"details": "Unauthorised Access"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        serializer = ResourceSerializer(resource)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        resource.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_resource(request):
    if request.method != "POST":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
    token_owner = Token.objects.get(key=token).user

    resource_content = request.data.get("content", None)

    if resource_content:
        new_resource = Resource(creator=token_owner, content=resource_content)

        try:
            new_resource.save()
        except QuotaExceededError as e:
            return Response({"details": e.message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = ResourceSerializer(new_resource)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"details": "Incomplete parameter"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def resource_quota(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method == "GET":
        try:
            resource_info = UserResourceInfo.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response({"details": "No quota set. Please set a quota for this user"},
                            status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserResourceInfoSerializer(resource_info)

            return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        obj, created = UserResourceInfo.objects.get_or_create(user=user)
        quota = request.data.get('quota', 0)

        obj.quota = quota
        obj.save()

        serializer = UserResourceInfoSerializer(obj)

        if created:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
