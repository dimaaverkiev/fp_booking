from _pyrepl.commands import refresh
from datetime import date, timedelta
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from django.db.models.functions import ExtractWeekDay
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User
from accounts.serializers import TenantSignupSerializer, LandlordSignupSerializer
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


def set_jwt_cookie(response, user):
    from datetime import datetime, timezone
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    access_expiry = datetime.fromtimestamp(access_token['exp'], timezone.utc)
    refresh_expiry = datetime.fromtimestamp(refresh_token['exp'], timezone.utc)

    response.set_cookie(
        key='access_token',
        value=str(access_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=access_expiry,
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh_token),
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry,
    )


class BaseSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = Response(serializer.data, status=status.HTTP_201_CREATED)

        set_jwt_cookie(response, user)

        return response


class LandlordSignupView(BaseSignupView):
    serializer_class = LandlordSignupSerializer


class TenantSignupView(BaseSignupView):
    serializer_class = TenantSignupSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]
    pass









