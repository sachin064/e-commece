from django.shortcuts import render
from django.utils import timezone

from .models import User
from rest_framework import viewsets, decorators
from .serializers import UserSerializer, UserDetailSerializer, PasswordChangeSerializer
from .utils.response import CommonResponse


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):  # done
        response = {'code': 200}
        try:
            users = self.queryset.exclude(id=request.user.id)
            users = users.exclude(is_deleted=True)
            serializer = UserSerializer(users, many=True)
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "users fetched successfully",
                'data': serializer.data
            })
        except:
            response.update({
                'status_code': 204,
                'message': "Error fetching users"
            })
        return CommonResponse(response).get_response()

    def retrieve(self, request, pk=None, *args, **kwargs):  # done
        response = {'code': 200}
        try:
            user = User.objects.get(pk=pk)
            user_serializer = UserDetailSerializer(user)
            data = user_serializer.data
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "User details fetched successfully",
                'data': data
            })
        except:
            response.update({
                'message': "Error in getting user Details"
            })
        return CommonResponse(response).get_response()

    def create(self, request, *args, **kwargs):  # done
        response = {'code': 201}
        try:
            user_data = request.data
            user_data.update({"is_first_login": True})
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                serializer = serializer.save(created_by=request.user)
                response.update({
                    'status': CommonResponse.STATUS_SUCCESS,
                    'message': "user created successfully",
                    'data': serializer.data
                })
            else:
                response.update({
                    'code': 400,
                    'message': "error creating user"
                })
        except:
            response = {
                'code': 400,
                'message': "Cant create user, Bad Request"
            }
        return CommonResponse(response).get_response()

    def destroy(self, request, pk=None, *args, **kwargs):  # done
        response = {'code': 204}
        try:
            user = User.objects.get(pk=pk)  # check
            user.is_deleted = True
            user.is_active = False
            user.save()
            response.update({
                'status': CommonResponse.STATUS_SUCCESS,
                'message': "User Deleted successfully",
            })
        except:
            response.update({
                'message': "Error in deleting user"
            })
        return CommonResponse(response).get_response()

    @decorators.action(methods=['POST'], detail=False, url_path='reset-password')
    def reset_password(self, request):
        response = {'code': 400}
        try:
            serializer = PasswordChangeSerializer(data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                response.update({
                    'code': 200,
                    'status': CommonResponse.STATUS_SUCCESS,
                    'message': 'password reset successful',
                    'data': serializer.data
                })
            else:
                response.update({
                    'message': 'please provide valid credentials'
                })
        except:
            response.update({
                'code': 400,
                'message': "Error resetting password"
            })
        return CommonResponse(response).get_response()

    def update(self, request, pk=None, *args, **kwargs):
        response = {'code': 400}
        try:
            user = User.objects.get(pk=pk)
            user.groups.clear()
            user_serializer = UserDetailSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save(updated_by=request.user, updated_on=timezone.now())
                response.update({
                    'code': 200,
                    'status': CommonResponse.STATUS_SUCCESS,
                    'message': 'user updated successfully',
                    'data': user_serializer.data
                })
            else:
                response.update({
                    'message': "Error updating user",
                })
        except:
            response.update({
                'message': 'Error updating user',
            })
        return CommonResponse(response).get_response()
