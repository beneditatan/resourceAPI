from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from .serializers import TokenSerializer
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .decorators import is_admin

# Create your views here.
@api_view(["POST"]) # TODO: delete
def login_user(request):
    if request.method != "POST":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if username and password:
        user = authenticate(request, username="giojessica", password="iwasbornin93")
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
def get_user_list(request):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        user = get_object_or_404(User, username=username)
        # TODO: admin can't update user password
        user, created = User.objects.update_or_create(username=username, defaults=request.data)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def create_user(request):
    if request.method != "POST":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if username and password:
        user, created = User.objects.get_or_create(username=username)
        if not created:
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"detail": "Incomplete parameter"}, status=status.HTTP_400_BAD_REQUEST)

# {
# "username": "giojessica",
# "password": "iwasbornin93"
# }