from rest_framework import serializers
from apartments.models import ApartmentAddress, FederalState
from apartments.serializers.federal_state_serializers import ListFederalStateSerializer


class ListApartmentAddressSerializer(serializers.ModelSerializer):
    federal_state = ListFederalStateSerializer()

    class Meta:
        model = ApartmentAddress
        fields = ('id', 'street', 'house_number', 'index_number', 'city', 'federal_state', 'country')



class CreateApartmentAddressSerializer(serializers.ModelSerializer):
    federal_state = serializers.PrimaryKeyRelatedField(queryset=FederalState.objects.all())
    country = serializers.CharField(read_only=True)

    class Meta:
        model = ApartmentAddress
        fields = ('street', 'house_number', 'index_number', 'city', 'federal_state', 'country')

    def validate_index_number(self, value):
        for vel in value:
            if not vel.isdigit():
                raise serializers.ValidationError('Index number must be digit')

        return value




class ShortInfoApartmentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentAddress
        fields = ('id', 'city', 'country')


class UpdateApartmentAddressSerializer(serializers.ModelSerializer):
    street = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    house_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    index_number = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    city = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    federal_state = serializers.PrimaryKeyRelatedField(queryset=FederalState.objects.all(), allow_null=True, required=False)

    class Meta:
        model = ApartmentAddress
        fields = ('street', 'house_number', 'index_number', 'city', 'federal_state', 'country')
        read_only_fields = ('country',)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value not in [None, ""]:
                setattr(instance, attr, value)

        instance.save()
        return instance









