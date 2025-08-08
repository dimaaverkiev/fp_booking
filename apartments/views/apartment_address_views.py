from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apartments.models import ApartmentAddress
from apartments.serializers.apartment_adress_serializers import (ListApartmentAddressSerializer,
                                                                 CreateApartmentAddressSerializer,
                                                                 UpdateApartmentAddressSerializer,
                                                                 ShortInfoApartmentAddressSerializer,
                                                                )
from accounts.permission import IsLandlordUser, IsOwnerLandlordOrReadOnly




class CreateApartmentAddressView(ListCreateAPIView):
    permission_classes = [IsLandlordUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListApartmentAddressSerializer
        return CreateApartmentAddressSerializer

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return ApartmentAddress.objects.filter(apartment__owner=landlord)




class UpdateDeleteApartmentAddressView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerLandlordOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateApartmentAddressSerializer
        elif self.request.method == 'DELETE':
            return ShortInfoApartmentAddressSerializer

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return ApartmentAddress.objects.filter(apartment__owner=landlord)









