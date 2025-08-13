from django.utils import timezone
from rest_framework import serializers
from accounts.models import LandlordUser
from apartments.models import Apartment, Category, ApartmentAddress
from apartments.serializers.category_serializers import ListCategorySerializer
from apartments.serializers.apartment_adress_serializers import ListApartmentAddressSerializer, \
    ShortInfoApartmentAddressSerializer, CreateApartmentAddressSerializer, UpdateApartmentAddressSerializer


class ShortInfoApartmentSerializer(serializers.ModelSerializer):
    address = ShortInfoApartmentAddressSerializer()

    class Meta:
        model = Apartment
        fields = ('id', 'title', 'price', 'address', 'rooms', 'booking_count')




class ListApartmentSerializer(serializers.ModelSerializer):
    category = ListCategorySerializer()
    address = ListApartmentAddressSerializer()

    class Meta:
        model = Apartment
        fields = ('id', 'title', 'description', 'category', 'price', 'rooms', 'created_at', 'address', 'booking_count')




class CreateApartmentSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    address = CreateApartmentAddressSerializer()

    class Meta:
        model = Apartment
        fields = ('title', 'description', 'category', 'price', 'rooms', 'created_at', 'owner', 'address', 'booking_count')
        read_only_fields = ('owner', 'created_at', 'booking_count')


    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value

    def validate_rooms(self, value):
        if value < 1:
            raise serializers.ValidationError('Rooms must be minimum 1')
        return value

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = ApartmentAddress.objects.create(**address_data)

        validated_data['address'] = address
        landlord = LandlordUser.objects.get(user=self.context['request'].user)
        validated_data['owner'] = landlord
        return super().create(validated_data)




class UpdateApartmentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    price = serializers.DecimalField(allow_null=True, required=False, decimal_places=2, max_digits=10)
    rooms = serializers.DecimalField(allow_null=True, required=False, decimal_places=1, max_digits=4)
    address = UpdateApartmentAddressSerializer(allow_null=True, required=False)

    class Meta:
        model = Apartment
        fields = ('title', 'description', 'category', 'price', 'rooms', 'updated_at', 'address', 'is_active')
        read_only_fields = ('updated_at',)

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                if value not in [None, ""]:
                    setattr(address, attr, value)
            address.save()

        for attr, value in validated_data.items():
            if value not in [None, ""]:
                setattr(instance, attr, value)

        instance.updated_at = timezone.now()

        instance.save()
        return instance


