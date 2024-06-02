from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import serializers

from messaging.models import FileType
from messaging.services.messaging_service import MessagingService


class SendMessageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    class InputSerializer(serializers.Serializer):
        receiver = serializers.CharField()
        content = serializers.CharField()
        attachment = serializers.FileField(required=False, allow_null=True)
        attachment_type = serializers.ChoiceField(choices=FileType.choices, required=False, allow_null=True)

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        success = MessagingService(request.user).send_message(**input_serializer.validated_data)
        if success:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Attachment type is required when an attachment is provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
