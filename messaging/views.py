from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import serializers

from messaging.models import FileType
from messaging.serializers import AccountSerializer, MessageSerializer
from messaging.services.messaging_service import MessagingService


class MessageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    class PostInputSerializer(serializers.Serializer):
        receiver = serializers.CharField()
        content = serializers.CharField()
        attachment = serializers.FileField(required=False, allow_null=True)
        attachment_type = serializers.ChoiceField(choices=FileType.choices, required=False, allow_null=True)

    def get(self, request):
        user_chats = MessagingService(request.user).get_user_chats()
        output_serializer = AccountSerializer(user_chats, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        input_serializer = self.PostInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        success = MessagingService(request.user).send_message(**input_serializer.validated_data)
        if success:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Attachment type is required when an attachment is provided."},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetChatView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username=None):
        chat_messages = MessagingService(request.user).get_user_chat(username)
        output_serializer = MessageSerializer(chat_messages, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)


class GetUnreadMessagesView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_messages = MessagingService(request.user).get_user_unread_messages()
        output_serializer = MessageSerializer(chat_messages, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
