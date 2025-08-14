from django.urls import path
from bookings.views import CreateListBookingView, LandlordUpdateStatusBookingView, DeleteBookingView, LandlordListBookingView




urlpatterns = [
    path('create_list_booking/', CreateListBookingView.as_view(), name='create_list_booking'),
    path('landlord_status_update/<int:pk>/', LandlordUpdateStatusBookingView.as_view(), name='landlord_status_update'),
    path('delete_booking/<int:pk>/', DeleteBookingView.as_view(), name='delete_booking'),
    path('landlord_booking_list/', LandlordListBookingView.as_view(), name='landlord_booking_list'),
]










