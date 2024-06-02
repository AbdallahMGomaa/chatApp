from rest_framework.generics import CreateAPIView
from auth_app.serializers import SignupSerializer


class SignupView(CreateAPIView):
    serializer_class = SignupSerializer
