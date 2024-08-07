from django.urls import path
from .views import (ChatListView,
                    CreateChatView,
                    ChatView,
                    EditMessageView,
                    DeleteMessageView,
                    MembersView,
                    ReplyView,
                    CheckOnlineStatus,
                    MessageList,
                    MessageDetail,
                    MessageFullDetail,
                    UserChats,
                    UserMessagesList,
                    )

app_name = 'messenger'
urlpatterns = [
    path('', ChatListView.as_view(), name='index'),
    path('create_chat/', CreateChatView.as_view(), name='create_chat'),
    path('<int:pk>/', ChatView.as_view(), name='chat'),
    path('delete_message/<int:pk>/', DeleteMessageView.as_view(), name='delete_message'),
    path('edit_message/<int:pk>/', EditMessageView.as_view(), name='edit_message'),
    path('members/<int:pk>/', MembersView.as_view(), name='members'),
    path('reply/', ReplyView.as_view(), name='reply'),
    path('online_status/', CheckOnlineStatus.as_view(), name='online_status'),
    path('messages/', MessageList.as_view()),
    path('messages/<int:pk>/', MessageDetail.as_view()),
    path('message_details/<int:pk>/', MessageFullDetail.as_view()),
    path('user_chats/<int:user_id>/', UserChats.as_view()),
    path('user_messages/<int:user_id>',UserMessagesList.as_view())
]