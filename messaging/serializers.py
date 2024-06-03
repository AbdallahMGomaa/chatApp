from rest_framework import serializers
from .models import Message, Attachment, Account, FileType


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_seen')





