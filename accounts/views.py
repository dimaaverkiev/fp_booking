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
from accounts.serializers import RegisterSerializerTenant, RegisterSerializerLandlord
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
    # permission_classes = [AllowAny]

    def _post(self, request, role_serializer):
        serializer = role_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except Exception as e:
                return Response({"detail" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

            response = Response({'user': {
                                        'first_name': user.first_name,
                                        'last_name': user.last_name,
                                        'email': user.email,
                    }
            }, status=status.HTTP_201_CREATED)

            set_jwt_cookie(response, user)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LandlordSignupView(BaseSignupView):
    permission_classes = [AllowAny]

    def post(self, request):
        return self._post(request, RegisterSerializerLandlord)



class TenantSignupView(BaseSignupView):
    permission_classes = [AllowAny]

    def post(self, request):
        return self._post(request, RegisterSerializerTenant)


class LoginView(APIView):
    permission_classes = [AllowAny]
    pass









