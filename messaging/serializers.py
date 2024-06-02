from rest_framework import serializers
from .models import Message, Attachment, Account, FileType


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email')


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('id', 'link', 'type')


class MessageSerializer(serializers.ModelSerializer):
    sender = AccountSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'attachments')

    def create(self, validated_data):
        attachments_data = self.context.get('attachments_data', [])
        message = Message.objects.create(**validated_data)
        for attachment_data in attachments_data:
            Attachment.objects.create(message=message, **attachment_data)
        return message


class MessageCreateSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, write_only=True)

    class Meta:
        model = Message
        fields = ('receiver', 'content', 'attachments')

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments')
        validated_data['sender'] = self.context['request'].user
        message = Message.objects.create(**validated_data)
        for attachment_data in attachments_data:
            Attachment.objects.create(message=message, **attachment_data)
        return message
