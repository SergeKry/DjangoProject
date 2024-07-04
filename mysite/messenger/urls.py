from django.urls import path
from .views import ChatListView, CreateChatView, ChatView, CreateMessageView
from . import views

app_name = 'messenger'
urlpatterns = [
    path('', ChatListView.as_view(), name='index'),
    path('create_chat/', CreateChatView.as_view(), name='create_chat'),
    path('<int:pk>/', ChatView.as_view(), name='chat'),
    path('<int:pk>/send_message/', CreateMessageView.as_view(), name='send_message'),
    path('delete_message/<int:pk>/', views.delete_message, name='delete_message'),
    path('edit_message_form/<int:pk>/', views.edit_message_form, name='edit_message_form'),
    path('update_message', views.update_message, name='update_message'),
    path('members/<int:pk>/', views.members, name='members'),
]