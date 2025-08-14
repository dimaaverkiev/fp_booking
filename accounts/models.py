from django.contrib.auth.base_user import  BaseUserManager
from django.contrib.auth.models import  AbstractUser
from django.db import models
from django.conf import settings




class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Need to provide email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("super user must have is_staff and is_superuser")

        return self.create_user(email, password, **extra_fields)




class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    username = None
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    birthday = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    passport_id = models.CharField(max_length=255)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} <{self.email}>'




class LandlordUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='landlord_user')




class TenantUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenant_user')









