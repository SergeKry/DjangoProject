from django.urls import path

from . import views

app_name = 'messenger'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('<int:pk>/', views.chat, name='chat'),
    path('send_message/', views.send_message, name='send_message'),
    path('delete_message/<int:pk>/', views.delete_message, name='delete_message'),
    path('edit_message_form/<int:pk>/', views.edit_message_form, name='edit_message_form'),
    path('update_message', views.update_message, name='update_message'),
    path('members/<int:pk>/', views.members, name='members'),
]