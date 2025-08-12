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


    def validate(self, attrs):
        booking = attrs.get('booking')

        # Проверка: отзыв уже существует?
        if Review.objects.filter(booking=booking).exists():
            raise serializers.ValidationError(
                {"booking": "Отзыв для этой брони уже был оставлен."}
            )

        return attrs


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields['booking'].queryset = Booking.objects.filter(user=user)


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




