from django.db import models
from django.contrib.auth.models import User
from category.models import Category
# Create your models here.



class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    hasbeensell = models.IntegerField(default=0,blank=True, null=True)
    evaluate = models.FloatField(null=True, blank=True, default=0)
    create_at = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return str(self.name)
    
    
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product =  models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.TextField()
    star = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
