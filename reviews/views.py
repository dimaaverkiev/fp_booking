from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from accounts.permission import IsLandlordUser, IsTenantUser
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
        tenant = getattr(self.request.user, 'tenant_user', None)
        return Review.objects.filter(user=tenant)




class LandlordListReviewView(ListAPIView):
    permission_classes = [IsLandlordUser | IsAdminUser]
    serializer_class = ListReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('booking__apartment', 'rating')
    ordering_fields = ('rating', 'created_at')

    def get_queryset(self):
        landlord = getattr(self.request.user, 'landlord_user', None)
        return Review.objects.filter(booking__apartment__owner=landlord, booking__apartment__is_active=True)




class UpdateDeleteReviewView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsTenantUser | IsAdminUser]
    serializer_class =  UpdateDeleteReviewSerializer

    def get_queryset(self):
        tenant = getattr(self.request.user, 'tenant_user', None)
        return Review.objects.filter(user=tenant)




class ApartmentListReviewView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('rating',)
    ordering_fields = ('rating', 'created_at')

    def get_queryset(self):
        apartment_id = self.kwargs.get('apartment_id')
        return Review.objects.filter(
            booking__apartment__id=apartment_id,
            booking__apartment__is_active=True
        )


