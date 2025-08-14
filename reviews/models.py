from django.db import models
from accounts.models import TenantUser
from bookings.models import Booking




class Review(models.Model):
    RATING_CHOICES = [
        ('1', 'Very poor'),
        ('2', 'Poor'),
        ('3', 'Average'),
        ('4', 'Good'),
        ('5', 'Excellent'),
    ]

    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    review_text = models.TextField()
    user = models.ForeignKey(TenantUser, on_delete=models.CASCADE, related_name='reviews')
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(fields=['booking'], name='unique_booking_review')
        ]

    def __str__(self):
        return f'{self.booking} {self.rating} {self.review_text}'