from django.urls import path
from .views import MessageView, GetChatView, GetUnreadMessagesView


urlpatterns = [
    path('messages/', MessageView.as_view(), name='send_message'),
    path('messages/unread/', GetUnreadMessagesView.as_view(), name='unread_messages'),
    path('messages/<str:username>/', GetChatView.as_view(), name='chat_messages'),
    # path('messages/history/', MessagesHistoryView.as_view(), name='messages_history'),
]



