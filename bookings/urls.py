from django.urls import path
from bookings.views import CreateListBookingView, LandlordListUpdateStatusBookingView, DeleteBookingView

urlpatterns = [
    path('create_list_booking/', CreateListBookingView.as_view(), name='create_list_booking'),
    path('landlord_list_status_update', LandlordListUpdateStatusBookingView.as_view(), name='landlord_list_status_update'),
    path('delete_booking/', DeleteBookingView.as_view(), name='delete_booking'),
]










