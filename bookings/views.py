from datetime import timedelta
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from accounts.permission import IsLandlordUser, IsTenantUser, IsOwnerTenantOrReadOnly
from bookings.models import Booking
from bookings.serializers import ListBookingSerializer, CreateBookingSerializer, StatusUpdateBookingSerializer




class CreateListBookingView(ListCreateAPIView):
    permission_classes = [IsTenantUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['start_date', 'end_date', 'status']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListBookingSerializer
        return CreateBookingSerializer

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant_user', None)
        return Booking.objects.filter(user=tenant)




class LandlordListBookingView(ListAPIView):
    permission_classes = [IsLandlordUser | IsAdminUser]
    serializer_class = ListBookingSerializer

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return Booking.objects.filter(apartment__owner=landlord)




class LandlordUpdateStatusBookingView(RetrieveUpdateAPIView):
    permission_classes = [IsLandlordUser | IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListBookingSerializer
        return StatusUpdateBookingSerializer

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return Booking.objects.filter(apartment__owner=landlord)




class DeleteBookingView(DestroyAPIView):
    permission_classes = [IsOwnerTenantOrReadOnly | IsAdminUser]

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant_user', None)
        return Booking.objects.filter(user=tenant)

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.start_date <= timezone.now().date():
            return Response({"error": "You cannot delete a booking that has started or finished."}, status=400)

        if booking.start_date - timedelta(days=7) <= timezone.now().date() and booking.status == 'A':
            return Response({"error": "You cannot delete a booking 7 days before start."}, status=400)

        apartment = booking.apartment
        if apartment.booking_count > 0:
            apartment.booking_count -= 1
            apartment.save(update_fields=['booking_count'])

        return super().destroy(request, *args, **kwargs)























