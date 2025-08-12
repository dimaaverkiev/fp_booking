from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('accounts.urls')),
    path('apartments/', include('apartments.urls')),
    path('bookings/', include('bookings.urls')),
    path('reviews/', include('reviews.urls')),
]
