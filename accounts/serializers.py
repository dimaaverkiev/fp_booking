from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from accounts.models import LandlordUser, TenantUser
from django.core.exceptions import ValidationError as DjangoValidationError



User = get_user_model()

class BaseSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    birthday = serializers.DateField()
    address = serializers.CharField()
    passport_id = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_birthday(self, value):
        today = date.today()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 18:
            raise serializers.ValidationError("User must be at least 18 years old.")
        return value


    def validate_email(self, value):
        return value.lower()


    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value



class LandlordSignupSerializer(BaseSignupSerializer):
    is_landlord = serializers.SerializerMethodField(read_only=True)

    def get_is_landlord(self, obj):
        return hasattr(obj, 'landlord_user')


    def create(self, validated_data):
        email = validated_data.pop('email').lower()
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        birthday = validated_data.pop('birthday')
        address = validated_data.pop('address')
        passport_id = validated_data.pop('passport_id')

        with transaction.atomic():
            user = User.objects.filter(email=email).first()
            if user:
                if hasattr(user, 'landlord_user'):
                    raise serializers.ValidationError("Landlord already exists.")
                user.first_name = first_name
                user.last_name = last_name
                user.birthday = birthday
                user.address = address
                user.passport_id = passport_id
                user.updated_at = timezone.now()

                if password and not user.has_usable_password():
                    user.set_password(password)

                user.save()

            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    birthday=birthday,
                    address=address,
                    passport_id=passport_id,
                )

            LandlordUser.objects.create(user=user)

        return user



class TenantSignupSerializer(BaseSignupSerializer):
    is_tenant = serializers.SerializerMethodField(read_only=True)

    def get_is_tenant(self, obj):
        return hasattr(obj, 'tenant_user')

    def create(self, validated_data):
        email = validated_data.pop('email').lower()
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        birthday = validated_data.pop('birthday')
        address = validated_data.pop('address')
        passport_id = validated_data.pop('passport_id')

        with transaction.atomic():
            user = User.objects.filter(email=email).first()
            if user:
                if hasattr(user, 'tenant_user'):
                    raise serializers.ValidationError("Tenant already exists.")
                user.first_name = first_name
                user.last_name = last_name
                user.birthday = birthday
                user.address = address
                user.passport_id = passport_id
                user.updated_at = timezone.now()

                if password and not user.has_usable_password():
                    user.set_password(password)

                user.save()

            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    birthday=birthday,
                    address=address,
                    passport_id=passport_id,
                )

            TenantUser.objects.create(user=user)

        return user



class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    last_name = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    address = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    passport_id = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'passport_id', 'updated_at', 'email']
        read_only_fields = ['updated_at', 'email']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if value not in [None, ""]:
                setattr(instance, attr, value)

        instance.updated_at = timezone.now()
        instance.save()
        return instance








