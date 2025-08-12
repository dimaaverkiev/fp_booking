from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apartments.models import Apartment
from apartments.serializers.apartment_serializers import (ListApartmentSerializer, DeleteApartmentSerializer,
                                                          CreateApartmentSerializer, UpdateApartmentSerializer,
                                                          )
from accounts.permission import IsLandlordUser, IsOwnerLandlordOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from apartments.views.filters import ApartmentFilter


class CreateListApartmentView(ListCreateAPIView):
    permission_classes = [IsLandlordUser]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['created_at', 'booking_count']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListApartmentSerializer
        return CreateApartmentSerializer

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return Apartment.objects.filter(owner=landlord, is_active=True)



class DetailApartmentView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListApartmentSerializer
    queryset = Apartment.objects.filter(is_active=True)


    filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter,)
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'booking_count', 'price']
    filterset_class = ApartmentFilter



class UpdateDeleteApartmentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerLandlordOrReadOnly | IsAdminUser]
    queryset = Apartment.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateApartmentSerializer
        elif self.request.method == 'DELETE':
            return DeleteApartmentSerializer
        else:
            return ListApartmentSerializer


    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return Apartment.objects.filter(owner=landlord, is_active=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



