from django.db import models
from .sms_util import send_sms
from django.utils import timezone


class Customer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Order(models.Model):
    item = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)  # Use DateTimeField with default=timezone.now
    customer = models.ForeignKey(Customer, related_name="orders", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            message = (
                f"Dear {self.customer.name}, your order for {self.item} "
                f"has been placed successfully. Total: {self.amount}."
            )
            send_sms(self.customer.phone_number, message)

    def __str__(self):
        return f"{self.item} - {self.amount:.2f}" 




