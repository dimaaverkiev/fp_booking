from rest_framework import serializers
from apartments.models import Apartment, Category, ApartmentAddress
from apartments.serializers.category_serializers import ListCategorySerializer
from apartments.serializers.apartment_adress_serializers import ListApartmentAddressSerializer, ShortInfoApartmentAddressSerializer





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
    address = serializers.PrimaryKeyRelatedField(queryset=ApartmentAddress.objects.all())

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
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)




class UpdateApartmentSerializer(serializers.ModelSerializer):
    title = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    description = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)
    price = serializers.DecimalField(allow_null=True, required=False, decimal_places=2, max_digits=10)
    rooms = serializers.DecimalField(allow_null=True, required=False, decimal_places=1, max_digits=4)
    address = serializers.PrimaryKeyRelatedField(queryset=ApartmentAddress.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Apartment
        fields = ('title', 'description', 'category', 'price', 'rooms', 'updated_at', 'address')
        read_only_fields = ('updated_at',)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value not in [None, ""]:
                setattr(instance, attr, value)

        instance.save()
        return instance




class DeleteApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = ('title', 'is_active')
        read_only_fields = ('title',)

    def update(self, instance, validated_data):
        instance.is_active = False
        instance.save()
        return instance
