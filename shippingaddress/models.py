from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from cart.models import Cart



class ShippingAddress(models.Model):
    CHOICES = [
        ("CHUA", "chua"),
        ("CO", "co"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    approved = models.CharField(max_length=4,choices=CHOICES,default="CHUA")
    received = models.BooleanField(default=False)
    total_items = models.IntegerField()
    total = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(max_length=100,null=True, blank=True)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100, null=True, blank=True)
    adderss = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    date_added =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adderss}"

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_items = models.IntegerField()
    total = models.CharField(max_length=100,null=True, blank=True)
    description = models.TextField(max_length=100,null=True, blank=True)
    adderss = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=200)
    date_added =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adderss}"
