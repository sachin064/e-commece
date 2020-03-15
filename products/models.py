from django.db import models
from accounts.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField(upload_to="products/media/")
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, blank=True, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}-cart'
