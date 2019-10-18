from .constants import AUTHORIZATION_HEADER, ADMIN_GROUP
from rest_framework.response import Response
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework import status

def is_admin(groups):
    def outer_wrapper(func):
        def wrapper(request, *args):
            token = request.META.get(AUTHORIZATION_HEADER).split(" ")[1]
            user = Token.objects.get(key=token)
            group = Group.objects.get(name=ADMIN_GROUP)
            members = group.user_set.all()
            
            if user in members:
                return func(request, *args, **kwargs)
            else:
                return Response({"detail": "Forbidden access}"}, status=status.HTTP_403_FORBIDDEN)
        return wrapper
    return outer_wrapper