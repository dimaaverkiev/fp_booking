from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser

from accounts.permission import IsLandlordUser, IsTenantUser, IsOwnerTenantOrReadOnly
from reviews.models import Review
from reviews.serializers import ListReviewSerializer, CreateReviewSerializer, UpdateDeleteReviewSerializer


class CreateListReviewView(ListCreateAPIView):
    permission_classes = [IsTenantUser]
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('rating', 'created_at')

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ListReviewSerializer
        return CreateReviewSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant_user', None)
        return Review.objects.filter(user=tenant)




class LandlordListReviewView(ListAPIView):
    permission_classes = [IsLandlordUser | IsAdminUser]
    serializer_class = ListReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('booking__apartment', 'rating')
    ordering_fields = ('rating', 'created_at')

    def get_queryset(self):
        landlord = getattr(self.request, 'landlord_user', None)
        return Review.objects.filter(booking__apartment__owner=landlord)




class UpdateDeleteReviewView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTenantUser | IsAdminUser]
    serializer_class =  UpdateDeleteReviewSerializer

    def get_queryset(self):
        tenant = getattr(self.request, 'tenant_user', None)
        return Review.objects.filter(user=tenant)






