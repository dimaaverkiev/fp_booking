from accounts.models import LandlordUser
from django.db import models




class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'category_apartments'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name




class FederalState(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'federal_state'
        verbose_name = 'Federal State'
        verbose_name_plural = 'Federal States'

    def __str__(self):
        return self.name




class ApartmentAddress(models.Model):
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=5)
    index_number = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    federal_state = models.ForeignKey(FederalState, on_delete=models.CASCADE, related_name='apartment_addresses')
    country = models.CharField(max_length=50, default='Germany')

    class Meta:
        db_table = 'apartment_address'
        verbose_name = 'Apartment Address'
        verbose_name_plural = 'Apartment Addresses'

    def __str__(self):
        return f'{self.street} {self.house_number}, {self.index_number} {self.city}, {self.federal_state}, {self.country}'




class Apartment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='apartments')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    rooms = models.DecimalField(decimal_places=1, max_digits=4)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    owner = models.ForeignKey(LandlordUser, on_delete=models.CASCADE, related_name='apartments')
    address = models.OneToOneField(ApartmentAddress, on_delete=models.CASCADE, related_name='apartment')
    booking_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'apartment'
        verbose_name = 'Apartment'
        verbose_name_plural = 'Apartments'
        ordering = ['-booking_count']

    def __str__(self):
        return self.title


