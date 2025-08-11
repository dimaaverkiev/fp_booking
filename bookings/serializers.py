from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.models import TenantUser
from apartments.models import Apartment
from apartments.serializers.apartment_serializers import ShortInfoApartmentSerializer
from bookings.models import Booking




class CreateBookingSerializer(ModelSerializer):
    apartment = serializers.PrimaryKeyRelatedField(queryset=Apartment.objects.all())

    class Meta:
        model = Booking
        fields = ('apartment', 'user', 'status', 'start_date', 'end_date', 'total_price', 'booking_at')
        read_only_fields = ('booking_at', 'total_price', 'status')


    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        apartment = attrs.get('apartment')

        if start_date >= end_date:
            raise serializers.ValidationError("End date must be after start date.")

        overlap_exists = Booking.objects.filter(
            apartment=apartment,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exists()

        if overlap_exists:
            raise serializers.ValidationError("This apartment is already booked for the selected dates.")


        return attrs


    def create(self, validated_data):
        tenant = TenantUser.objects.get(user=self.context['request'].user)
        validated_data['user'] = tenant

        price = validated_data['apartment'].price
        days_count = (validated_data['end_date'] - validated_data['start_date']).days
        validated_data['total_price'] = price * days_count

        return super().create(validated_data)



class ListBookingSerializer(ModelSerializer):
    apartment = ShortInfoApartmentSerializer()

    class Meta:
        model = Booking
        fields = ('id', 'apartment', 'status', 'user', 'start_date', 'end_date', 'total_price', 'booking_at')



class StatusUpdateBookingSerializer(ModelSerializer):
    apartment = ShortInfoApartmentSerializer()

    class Meta:
        model = Booking
        fields = ('id', 'apartment', 'status', 'user', 'start_date', 'end_date', 'total_price', 'booking_at')
        read_only_fields = ('id', 'apartment', 'user', 'start_date', 'end_date', 'total_price', 'booking_at')






