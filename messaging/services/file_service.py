import os
import magic
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class UnsafeFileException(Exception):
    pass


class FileService:
    def __init__(self):
        self.storage = FileSystemStorage(location=settings.MEDIA_ROOT)
        self.safe_mime_types = [
            'image/jpeg',
            'image/png',
            'application/pdf',
            'audio/mpeg',
            'video/mp4'
            # Add other safe MIME types as needed
        ]

    def is_safe_file(self, file):
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(file.read(1024))
        file.seek(0)
        if file_mime_type not in self.safe_mime_types:
            raise UnsafeFileException(f"Unsafe file type: {file_mime_type}")
        return True

    def save_file(self, file):
        self.is_safe_file(file)
        filename = self.storage.save(file.name, file)
        file_url = os.path.join(settings.MEDIA_URL, filename)
        return file_url
