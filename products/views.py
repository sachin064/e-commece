from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from rest_framework.decorators import api_view

from accounts.utils.response import CommonResponse
from .models import Products, Category, Cart
from .serializers import ProductSerializer, ProductDetailSerializer, CartSerializer, CartDetailSerializer, \
    CategorySerializer, CategoryDetailSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    serializer_class = ProductDetailSerializer
    queryset = Products.objects.all()

    def list(self, request, *args, **kwargs):
        response = {'code': 200}
        try:
            products = self.queryset
            serializer = ProductSerializer(products, many=True)
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "all products fetched successfully",
                'data': serializer.data
            })
        except:
            response.update({
                'code': '400',
                'message': "failed to fetch all products"
            })
        return CommonResponse(response).get_response()

    def retrieve(self, request, pk=None, *args, **kwargs):
        response = {'code': 200}
        try:
            product = Products.objects.get(pk=pk)
            serializer = ProductDetailSerializer(product)
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "product details fetched successfully",
                'data': serializer.data
            })
        except:
            response.update({
                'code': 400,
                'message': "Error in fetching product details",
            })
        return CommonResponse(response).get_response()

    def create(self, request, *args, **kwargs):
        response = {'code': 201}
        try:
            product_data = request.data
            serializer = ProductSerializer(product_data)
            if serializer.is_valid():
                serializer.save()
                response.update({
                    'status': CommonResponse.STATUS_SUCCESS,
                    'message': "products added successfully",
                    'data': serializer.data
                })
            else:
                response.update({
                    'code': 400,
                    'message': "Error adding product",
                })
        except:
            response.update({
                'code': 400,
                'message': "Error adding product",
            })
        return CommonResponse(response).get_response()


class CategoryVIewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        response = {'code': 200}
        try:
            queryset = self.get_queryset()  # check
            serializer = CategorySerializer(queryset, many=True)
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "list of all categories fetched successfully",
                'data': serializer.data
            })
        except:
            response.update({
                'code': 400,
                'message': "error fetching list of categories",
            })
        return CommonResponse(response).get_response()


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def create(self, request, *args, **kwargs):
        response = {'code': 200}
        try:
            data = request.data
            serializer = CartSerializer(data)
            if serializer.is_valid():
                serializer.save()
                response.update({
                    'status': CommonResponse.STATUS_SUCCESS,
                    'message': "Cart added successfully",
                    'data': serializer.data
                })
            else:
                response.update({
                    'code': 400,
                    'message': "Error creating cart"
                })
        except:
            response.update({
                'code': 400,
                'message': "Error creating cart"
            })
        return CommonResponse(response).get_response()


from django.shortcuts import render


def index(request):
    return render(request, 'base.html')
