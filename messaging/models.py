from django.db import models

from auth_app.models import Account


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)


class FileType(models.TextChoices):
    AUDIO = 'audio', 'Audio'
    VIDEO = 'video', 'Video'
    IMAGE = 'image', 'Image'
    OTHER = 'other', 'Other'


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    link = models.URLField()
    type = models.CharField(choices=FileType.choices, default=FileType.OTHER.value, max_length=50)

