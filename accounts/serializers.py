from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'password', 'created_on', 'updated_on',
            'is_first_login', 'full_name', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='get_user_groups')
    permissions = serializers.SerializerMethodField('group_permissions')
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_first_login', 'created_by',
            'full_name', 'updated_by', 'updated_on', 'created_on')

    def group_permissions(self, obj):
        return obj.groups.first().permissions.values('id', 'name')


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    def validate(self, data):
        user = self.context['request'].user

        if not user.check_password(data.get('old_password')):
            raise serializers.ValidationError({"old_password": ["Please provide correct password"]})
        elif data.get('old_password') == data.get('new_password1'):
            raise serializers.ValidationError({"new_password": ["Please choose different password"]})
        elif data.get('new_password1') != data.get('new_password2'):
            raise serializers.ValidationError({"new_password": ["Passwords mismatch"]})
        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data.get('new_password1'))
        user.is_first_login = False
        user.save()
        return user
