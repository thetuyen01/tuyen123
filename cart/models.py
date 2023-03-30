from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from product.models import Product



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self) -> str:
        return str(self.user.username)
    
    @property
    def total_items_price(self):
        total=0
        orderitem = self.ortheritem_set.all()
        for i in orderitem:
            total += i.total_price
        return total
    @property
    def total_item(self):
        total=0
        orderitem = self.ortheritem_set.all()
        for i in orderitem:
            total += i.quantity
        return total

class OrtherItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.product.name)
    
    @property
    def total_price(self):
        total = int(self.quantity)*int(self.product.price)
        return total