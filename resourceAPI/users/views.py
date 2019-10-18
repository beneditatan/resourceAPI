from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(["GET"])
def get_user_list(request):
    if request.method != "GET":
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET", "PUT"])
def user_detail(request, username):
    if request.method == "GET":
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":

        return Response({"detail": "Creation successful"}, status=status.HTTP_202_ACCEPTED)
    else:
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

