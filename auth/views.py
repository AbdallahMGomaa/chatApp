from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from auth.serializers import SignupSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
