from django.db import transaction

from auth_app.models import Account
from messaging.models import Message, Attachment
from messaging.services.file_service import FileService, UnsafeFileException


class MessagingService:
    def __init__(self, sender):
        self.sender = sender
        self.file_service = FileService()

    @transaction.atomic
    def send_message(self, receiver, content, attachment=None, attachment_type=None):
        try:
            receiver = Account.objects.get(username=receiver)
        except Account.DoesNotExist:
            raise ValueError("Receiver does not exist")
        message_object = Message.objects.create(
            sender=self.sender,
            receiver=receiver,
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


