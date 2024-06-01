from django.db import models

from auth_app.models import Account


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class FileType(models.Choices):
    AUDIO = 'audio', 'Audio'
    VIDEO = 'video', 'Video'
    IMAGE = 'image', 'Image'
    OTHER = 'other', 'Other'


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    link = models.URLField()
    type = models.CharField(choices=FileType.choices, default=FileType.OTHER.value)

