from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Chat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'chat', 'text', 'created_at', 'replied_to', 'author']


class MessageDetailSerializer(MessageSerializer):
    author = UserSerializer(read_only=True)


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['name', 'created_at']