from rest_framework import serializers
from .models import Message, Attachment, Account, FileType


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')
    receiver_username = serializers.CharField(source='receiver.username')
    class Meta:
        model = Message
        fields = ('id', 'sender', 'receiver', 'content', 'timestamp', 'is_seen', 'sender_username', 'receiver_username')





