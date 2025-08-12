from django.utils import timezone
from rest_framework import serializers
from accounts.models import TenantUser
from bookings.models import Booking
from bookings.serializers import ListBookingSerializer
from reviews.models import Review




class CreateReviewSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(queryset=Booking.objects.none())

    class Meta:
        model = Review
        fields = ('rating', 'review_text', 'user', 'booking')
        read_only_fields = ('user', 'created_at')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user.tenant_user
        self.fields['booking'].queryset = Booking.objects.filter(user=user, end_date__lte=timezone.now())


    def validate(self, attrs):
        booking = attrs.get('booking')

        if Review.objects.filter(booking=booking).exists():
            raise serializers.ValidationError(
                {"booking": "Review already exists for this booking."}
            )

        return attrs


    def create(self, validated_data):
        tenant = TenantUser.objects.get(user=self.context['request'].user)
        validated_data['user'] = tenant

        return super().create(validated_data)




class ListReviewSerializer(serializers.ModelSerializer):
    booking = ListBookingSerializer()

    class Meta:
        model = Review
        fields = ('id', 'rating', 'review_text', 'user', 'booking', 'created_at')




class UpdateDeleteReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'rating', 'review_text')




