from rest_framework import serializers
from apartments.models import Category




class ListCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')




class CreateUpdateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance






