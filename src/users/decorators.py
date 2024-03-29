from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .constants import ADMIN_GROUP, AUTHORIZATION_HEADER
from .utils import is_member_of


def admin_only(func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
        user = Token.objects.get(key=token).user
        is_admin = is_member_of(user.username, ADMIN_GROUP)
        
        if is_admin:
            return func(request, *args, **kwargs)
        else:
            return Response({"detail": "Forbidden access"}, status=status.HTTP_403_FORBIDDEN)

    return wrapper
