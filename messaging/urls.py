from django.urls import path
from .views import SendMessageView

urlpatterns = [
    path('messages/send/', SendMessageView.as_view(), name='send_message'),
]