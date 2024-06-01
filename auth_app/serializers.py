from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.state import token_backend

from .models import Account
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    error_msg = 'No active account found with given credentials'

    def validate(self, attrs):
        token_payload = token_backend.decode(attrs.get('token'))
        try:
            user = get_user_model().objects.get(pk=token_payload['id'])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(self.error_msg)
        return super().validate(attrs)

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Account
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user

