from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import (TenantSignupView, LandlordSignupView, LoginView)

# router = DefaultRouter()
# router.register(r'login', LoginView, basename='login')

urlpatterns = [
    # path('', include(router.urls)),
    path('signup_tenant/', TenantSignupView.as_view(), name='signup_tenant'),
    path('signup_landlord/', LandlordSignupView.as_view(), name='signup_landlord'),
]










