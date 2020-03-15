from rest_framework import serializers
from .models import Products, Cart, Category


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('name', 'image', 'description', 'quantity', 'price', 'category')


class CartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('user', 'name', 'products')


class CategorySerializer(serializers.ModelSerializer):
    class Mets:
        model = Category
        fields = ('name', 'description')


class CategoryDetailSerializer(serializers.ModelSerializer):
    class Mets:
        model = Category
        fields = '__all__'
