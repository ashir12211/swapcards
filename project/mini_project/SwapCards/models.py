
from django.db import models
from django.contrib.auth.models import User

class selling_info(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('sold', 'Sold')
    ]
    username1 = models.CharField(max_length=150)
    card_number = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    giftcard_type = models.CharField(max_length=100)
    expiry = models.DateField(default='2025-12-31')
    giftcard_balance = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.giftcard_type} - {self.status}"


class PurchasedGiftCard(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=50)
    pin = models.CharField(max_length=50)
    giftcard_type = models.CharField(max_length=100)
    expiry = models.DateField()
    giftcard_balance = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buyer.username} bought {self.giftcard_type} on {self.purchased_at}"
