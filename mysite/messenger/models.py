from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='chats', blank=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=500)
    replied_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reply')

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.text


class MessageLog(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} created {self.message} at {self.time}'


class OnlineStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    online = models.BooleanField(default=False)
