from django.db import models
from apartments.models import Apartment
from accounts.models import TenantUser


class Booking(models.Model):
    STATUS_CHOICES = [
        ('A', 'Approved'),
        ('R', 'Rejected'),
        ('P', 'Pending'),
    ]

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(TenantUser, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookings'
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

