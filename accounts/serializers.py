from datetime import date
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from accounts.models import User
from django.core.exceptions import ValidationError as DjangoValidationError



class BaseRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birthday', 'address',
                  'passport_id', 'email', 'password']

    def validate_birthday(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("User must be at least 18 years old.")
        return value

    def validate_email(self, value):
        value = value.lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("User already exists.")
        return value

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def _create(self, validated_data, role_field):
        validated_data['email'] = validated_data['email'].lower()
        password = validated_data.pop('password')
        with transaction.atomic():
            user = User.objects.create_user(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                birthday=validated_data['birthday'],
                address=validated_data['address'],
                passport_id=validated_data['passport_id'],
                email=validated_data['email'],
                password=password,
            )
            if role_field == "is_landlord":
                user.is_landlord = True
            elif role_field == "is_tenant":
                user.is_tenant = True
            user.save()

        return user


class RegisterSerializerLandlord(BaseRegisterSerializer):
    def create(self, validated_data):
        return self._create(validated_data, 'is_landlord')


class RegisterSerializerTenant(BaseRegisterSerializer):
    def create(self, validated_data):
        return self._create(validated_data, 'is_tenant')



# {
# "first_name":"user_firstname",
# "last_name":"user_lastname",
# "email":"user1@user.com",
# "birthday":"1997-02-04",
# "address":"Munich",
# "passport_id":"FP12345FP",
# "password":"user1user1"
# }





