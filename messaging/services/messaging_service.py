from django.db import transaction
from django.db.models import Q

from auth_app.models import Account
from messaging.models import Message, Attachment
from messaging.services.file_service import FileService, UnsafeFileException


class MessagingService:
    def __init__(self, sender):
        self.user = sender
        self.file_service = FileService()

    def __get_peer(self, username):
        try:
            peer = Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise ValueError("Receiver does not exist")
        return peer

    @transaction.atomic
    def send_message(self, receiver, content, attachment=None, attachment_type=None):
        peer = self.__get_peer(receiver)
        message_object = Message.objects.create(
            sender=self.user,
            receiver=peer,
            content=content
        )

        if attachment:
            if attachment_type:
                try:
                    attachment_url = self.file_service.save_file(attachment)
                    Attachment.objects.create(
                        message=message_object,
                        type=attachment_type,
                        link=attachment_url
                    )
                except UnsafeFileException as e:
                    raise ValueError(str(e))
            else:
                return False
        return True

    def get_user_chats(self):
        sent_message_receiver_ids = (Message.objects.filter(sender=self.user)
                                     .values_list('receiver_id', flat=True)
                                     .distinct())
        received_message_sender_ids = (Message.objects.filter(receiver=self.user)
                                       .values_list('sender_id', flat=True)
                                       .distinct())
        distinct_user_ids = sent_message_receiver_ids.union(received_message_sender_ids)
        distinct_users = Account.objects.filter(id__in=distinct_user_ids)
        return distinct_users

    def get_user_chat(self, username):
        peer = self.__get_peer(username)

        chat_messages = Message.objects.filter(
            Q(Q(sender=self.user) & Q(receiver=peer)) | Q(Q(sender=peer) & Q(receiver=self.user))
        ).order_by('timestamp')
        chat_messages.filter(is_seen=False, sender=peer).update(is_seen=True)
        return chat_messages

    def get_user_unread_messages(self):
        chat_messages = Message.objects.filter(receiver=self.user, is_seen=False).order_by('timestamp')
        return chat_messages
