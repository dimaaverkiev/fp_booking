from rest_framework import serializers
from apartments.models import FederalState




class ListFederalStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederalState
        fields = ('id', 'name')




class CreateUpdateFederalStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederalState
        fields = ('name',)

    def create(self, validated_data):
        return FederalState.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance