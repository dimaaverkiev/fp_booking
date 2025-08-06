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
from accounts.permission import IsLandlordUser, IsTenantUser
from accounts.serializers import TenantSignupSerializer, LandlordSignupSerializer, UserUpdateSerializer
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

    def post(self, request, *args, **kwargs):
        from datetime import datetime, timezone

        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"detail": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_active:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            access_expiry = datetime.fromtimestamp(access_token['exp'], timezone.utc)
            refresh_expiry = datetime.fromtimestamp(refresh['exp'], timezone.utc)

            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
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
                value=str(refresh),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry,
            )
            return response
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token is None:
                return Response({"detail": "Refresh token not found."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError as e:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'message': 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


# {
# "email":"user1@user.com",
# "password":"user1user1"
# }


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LandlordUserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsLandlordUser]

    def delete(self, request):
        landlord_user = request.user.landlord_user

        if landlord_user:
            landlord_user.delete()

        return Response({'message':'landlord user deleted'}, status=status.HTTP_204_NO_CONTENT)


class TenantUserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsTenantUser]

    def delete(self, request):
        tenant_user = request.user.tenant_user

        if tenant_user:
            tenant_user.delete()

        return Response({'message':'tenant user deleted'}, status=status.HTTP_204_NO_CONTENT)







