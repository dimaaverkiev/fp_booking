from django.urls import path

from accounts.views import (TenantSignupView, LandlordSignupView, LoginView, LogoutView,)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/signup_tenant/', TenantSignupView.as_view(), name='signup_tenant'),
    path('api/signup_landlord/', LandlordSignupView.as_view(), name='signup_landlord'),
    path('api/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('api/login/', LoginView.as_view(), name="login"),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]










