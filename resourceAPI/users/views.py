from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .decorators import admin_only
from .serializers import TokenSerializer, UserSerializer


# Create your views here.
@api_view(["POST"]) # TODO: delete
def login_user(request):
    if request.method != "POST":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if email and password:
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"detail": "User is not registered"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            username = user.username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                token = Token.objects.create(user=user)
            except IntegrityError:
                # existing user
                token = Token.objects.get(user=user)

            serializer = TokenSerializer(token)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User is not registered"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def get_user_list(request):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PATCH", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def user_detail(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        user = get_object_or_404(User, username=username)
        
        if "password" in request.data:
            return Response({"detail": "Password update not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.update_or_create(username=username, defaults=request.data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    elif request.method =="DELETE":
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@admin_only
def create_user(request):
    if request.method != "POST":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    username = request.data.get("username", None)
    email = request.data.get("email", None)
    password = request.data.get("password", None)

    if username and password and email:
        user, created = User.objects.get_or_create(username=username)
        if not created:
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.email = email
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Incomplete parameter"}, status=status.HTTP_400_BAD_REQUEST)

# {
# "username": "giojessica",
# "password": "iwasbornin93"
# }
