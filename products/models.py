from django.db import models
from accounts.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=512)
    description = models.TextField(null=True, blank=True)


class Products(models.Model):
    name = models.CharField(max_length=512)
    image = models.ImageField(upload_to="media/")
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=512, blank=True, null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
