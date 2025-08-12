from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include('accounts.urls')),
    path('apartments/', include('apartments.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
]
