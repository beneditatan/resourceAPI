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

from .decorators import admin_only


# Create your views here.
