from django.contrib import admin
from .models import Chat, Message, MessageLog

admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(MessageLog)